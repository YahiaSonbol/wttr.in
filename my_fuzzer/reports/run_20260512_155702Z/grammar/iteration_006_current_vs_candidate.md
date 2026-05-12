# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 6 |
| From | run_20260512_155702Z_baseline_iteration_006 |
| To | run_20260512_155702Z_candidate_iteration_006 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | searchparameter, LANG_SUFFIX, query |

## Diff

```diff
--- run_20260512_155702Z_baseline_iteration_006
+++ run_20260512_155702Z_candidate_iteration_006
@@ -45,7 +45,7 @@
 
 // helper token for language suffix used in PNG routes
 LANG_SUFFIX
-    : 'lang=' STRING
+    : 'lang=' (STRING | HEX | ('en'|'ru'|'de'|'es'|'fr'|'ja'|'zh'|'ko'|'ar'|'th'|'tr'|'hi'))
     ;
 
 search
@@ -56,9 +56,8 @@
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // mixed flag chain with regular key=value pair
+    | 'use_imperial' '=' ('1' | 'true' | 'yes')
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
-    // flag‑only chain allowing empty segments and repeated '&'
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))* )
     | 'lang' '=' STRING
     | 'format' '=' STRING
```
