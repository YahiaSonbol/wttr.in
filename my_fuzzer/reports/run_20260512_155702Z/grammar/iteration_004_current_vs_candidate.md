# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 4 |
| From | run_20260512_155702Z_baseline_iteration_004 |
| To | run_20260512_155702Z_candidate_iteration_004 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | LANG_SUFFIX, searchparameter, query |

## Diff

```diff
--- run_20260512_155702Z_baseline_iteration_004
+++ run_20260512_155702Z_candidate_iteration_004
@@ -35,8 +35,8 @@
     | 'moon' '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'moon' '@' CITY '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     // extended PNG routes with variable size and language suffixes, allowing optional flag chain after
-    | CITY '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
-    | 'moon' '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
+    | CITY '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png' ( '?' search )?
+    | 'moon' '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png' ( '?' search )?
     // colon‑prefixed API routes with optional full query strings
     | 'weather:' CITY ('?' search)?
     | 'forecast:' CITY ('?' search)?
@@ -45,7 +45,7 @@
 
 // helper token for language suffix used in PNG routes
 LANG_SUFFIX
-    : 'lang=' STRING
+    : 'lang=' ( 'en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi' )
     ;
 
 search
@@ -56,9 +56,8 @@
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // mixed flag chain with regular key=value pair
+    | 'use_imperial' '=' (DIGITS | STRING)
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
-    // flag‑only chain allowing empty segments and repeated '&'
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))* )
     | 'lang' '=' STRING
     | 'format' '=' STRING
```
