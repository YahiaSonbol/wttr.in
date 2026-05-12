# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 7 |
| From | run_20260512_155702Z_baseline_iteration_007 |
| To | run_20260512_155702Z_candidate_iteration_007 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | searchparameter, LANG_SUFFIX |

## Diff

```diff
--- run_20260512_155702Z_baseline_iteration_007
+++ run_20260512_155702Z_candidate_iteration_007
@@ -45,7 +45,7 @@
 
 // helper token for language suffix used in PNG routes
 LANG_SUFFIX
-    : 'lang=' STRING
+    : 'lang=' ('en' | 'de' | 'ru' | 'fr' | 'es' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
     ;
 
 search
@@ -56,6 +56,7 @@
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
+    | 'use_imperial' ('=' ( '1' | 'true' | 'yes' | string ))?
     // mixed flag chain with regular key=value pair
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
     // flag‑only chain allowing empty segments and repeated '&'
```
