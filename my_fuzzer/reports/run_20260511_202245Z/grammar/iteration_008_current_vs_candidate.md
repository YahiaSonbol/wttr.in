# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 8 |
| From | run_20260511_202245Z_baseline_iteration_008 |
| To | run_20260511_202245Z_candidate_iteration_008 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | query, searchparameter, CITY |

## Diff

```diff
--- run_20260511_202245Z_baseline_iteration_008
+++ run_20260511_202245Z_candidate_iteration_008
@@ -34,7 +34,6 @@
     | '?' 'format' '=' 'png'
     | 'moon' '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'moon' '@' CITY '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
-    // extended PNG routes with variable size and language suffixes, allowing optional flag chain after
     | CITY '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
     | 'moon' '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
     // colon‑prefixed API routes with optional full query strings
@@ -56,10 +55,10 @@
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // mixed flag chain with regular key=value pair
+    // pure flag‑only chain, e.g., "A&d&n"
+    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&' ('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+)* )
+    // mixed flag/key=value sequences, flags may appear before or after a key=value pair
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
-    // flag‑only chain allowing empty segments and repeated '&'
-    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))* )
     | 'lang' '=' STRING
     | 'format' '=' STRING
     | 'location' '=' STRING
@@ -105,6 +104,6 @@
     : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon'
     // generic city allowing optional size, language suffix, trailing underscores and percent‑encoding
     | [a-zA-Z]+ ('_' DIGITS 'x')? ('_'? 'lang=' (STRING | HEX))? ('_'*)?
-    // percent‑encoded city names like %E6%9C%AC%E5%9C%B0 (Tokyo in UTF‑8)
-    | (HEX)+
+    // percent‑encoded city names, allow multiple HEX blocks separated by optional underscores
+    | (HEX ('_'? HEX)*)
     ;
```
