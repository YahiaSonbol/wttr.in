from __future__ import annotations

import json
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .core import FuzzerConfig, run_command


MUTABLE_RULES = (
    "query",
    "search",
    "searchparameter",
    "string",
    "DIGITS",
    "HEX",
    "STRING",
    "CITY",
)

IMMUTABLE_RULES = (
    "url",
    "uri",
    "protocol",
    "host",
    "port",
    "PROTOCOL",
    "HOSTNAME",
    "PORTS",
)


@dataclass
class RuleUpdate:
    rule: str
    replacement: str


@dataclass
class MutationPlan:
    updates: list[RuleUpdate]
    rationale: str = ""


def _grammar_lines(grammar_text: str) -> list[str]:
    return grammar_text.splitlines(keepends=True)


def locate_rule_block(grammar_text: str, rule_name: str) -> tuple[int, int]:
    lines = _grammar_lines(grammar_text)
    offset = 0

    for idx, line in enumerate(lines):
        if line.strip() != rule_name:
            offset += len(line)
            continue

        end_offset = offset + len(line)
        for follow in lines[idx + 1 :]:
            end_offset += len(follow)
            if follow.strip() == ";":
                return offset, end_offset
        break

    raise ValueError(f"Rule `{rule_name}` was not found in the grammar.")


def extract_rule_block(grammar_text: str, rule_name: str) -> str:
    start, end = locate_rule_block(grammar_text, rule_name)
    return grammar_text[start:end].rstrip() + "\n"


def mutable_rule_context(grammar_text: str) -> str:
    return "\n".join(extract_rule_block(grammar_text, rule_name).rstrip() for rule_name in MUTABLE_RULES)


def immutable_rule_context(grammar_text: str) -> str:
    return "\n\n".join(extract_rule_block(grammar_text, rule_name).rstrip() for rule_name in IMMUTABLE_RULES)


def _first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    raise ValueError("Replacement block is empty.")


def normalize_rule_block(replacement: str, expected_rule_name: str) -> str:
    text = replacement.strip() + "\n"
    first_line = _first_nonempty_line(text)
    if first_line != expected_rule_name:
        raise ValueError(
            f"Replacement for `{expected_rule_name}` must start with the rule name on its own line; got `{first_line}`."
        )
    if not any(line.strip() == ";" for line in text.splitlines()):
        raise ValueError(f"Replacement for `{expected_rule_name}` must contain a semicolon line.")
    return text


def apply_mutation_plan(current_grammar: str, plan: MutationPlan) -> str:
    seen_rules: set[str] = set()
    candidate = current_grammar

    if not plan.updates:
        raise ValueError("The LLM response contained no rule updates.")

    for update in plan.updates:
        if update.rule in seen_rules:
            raise ValueError(f"Rule `{update.rule}` was updated more than once in one response.")
        seen_rules.add(update.rule)

        if update.rule not in MUTABLE_RULES:
            allowed = ", ".join(MUTABLE_RULES)
            raise ValueError(f"Rule `{update.rule}` is not mutable. Allowed rules: {allowed}.")

        replacement = normalize_rule_block(update.replacement, update.rule)
        start, end = locate_rule_block(candidate, update.rule)
        candidate = candidate[:start] + replacement + candidate[end:]

    for rule_name in IMMUTABLE_RULES:
        if extract_rule_block(candidate, rule_name) != extract_rule_block(current_grammar, rule_name):
            raise ValueError(f"Immutable rule `{rule_name}` changed; the agent must keep the local base URL fixed.")

    return candidate


def extract_json_object(raw_text: str) -> str:
    fenced_start = raw_text.find("```")
    if fenced_start != -1:
        fence = raw_text.find("\n", fenced_start)
        fenced_end = raw_text.find("```", fence + 1)
        if fence != -1 and fenced_end != -1:
            fenced_body = raw_text[fence + 1 : fenced_end].strip()
            if fenced_body.startswith("{"):
                raw_text = fenced_body

    start = raw_text.find("{")
    if start == -1:
        raise ValueError("Could not find a JSON object in the LLM response.")

    depth = 0
    in_string = False
    escaped = False

    for index in range(start, len(raw_text)):
        char = raw_text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return raw_text[start : index + 1]

    raise ValueError("The JSON object in the LLM response was not closed.")


def parse_mutation_plan(raw_text: str) -> MutationPlan:
    try:
        payload = json.loads(extract_json_object(raw_text))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Could not decode the LLM JSON response: {exc}") from exc

    updates_raw = payload.get("updates")
    if not isinstance(updates_raw, list):
        raise ValueError("The LLM response must contain an `updates` array.")

    updates: list[RuleUpdate] = []
    for index, entry in enumerate(updates_raw, start=1):
        if not isinstance(entry, dict):
            raise ValueError(f"Update #{index} is not an object.")
        rule = entry.get("rule")
        replacement = entry.get("replacement")
        if not isinstance(rule, str) or not rule.strip():
            raise ValueError(f"Update #{index} is missing a string `rule` field.")
        if not isinstance(replacement, str) or not replacement.strip():
            raise ValueError(f"Update #{index} is missing a string `replacement` field.")
        updates.append(RuleUpdate(rule=rule.strip(), replacement=replacement))

    rationale = payload.get("rationale", "")
    if not isinstance(rationale, str):
        rationale = str(rationale)

    return MutationPlan(updates=updates, rationale=rationale.strip())


def validate_candidate_grammar(config: FuzzerConfig, candidate_text: str) -> tuple[bool, str]:
    with tempfile.TemporaryDirectory(prefix="wttr-grammar-check-") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        grammar_file = temp_dir / "url.g4"
        out_dir = temp_dir / "generated"
        out_dir.mkdir(parents=True, exist_ok=True)
        grammar_file.write_text(candidate_text, encoding="utf-8")

        result = run_command(
            [
                "grammarinator-process",
                str(grammar_file),
                "-o",
                str(out_dir),
                "--no-actions",
            ],
            cwd=config.repo_root,
            check=False,
        )

        combined = (result.stdout or "") + "\n" + (result.stderr or "")
        if result.returncode != 0:
            return False, combined.strip()

        return True, combined.strip() or "grammarinator-process succeeded."
