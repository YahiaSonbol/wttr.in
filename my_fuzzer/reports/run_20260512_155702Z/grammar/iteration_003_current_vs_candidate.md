# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 3 |
| From | run_20260512_155702Z_baseline_iteration_003 |
| To | run_20260512_155702Z_candidate_iteration_003 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | searchparameter, query, LANG_SUFFIX |

## Diff

```diff
--- run_20260512_155702Z_baseline_iteration_003
+++ run_20260512_155702Z_candidate_iteration_003
@@ -34,18 +34,18 @@
     | '?' 'format' '=' 'png'
     | 'moon' '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'moon' '@' CITY '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
-    // extended PNG routes with variable size and language suffixes, allowing optional flag chain after
     | CITY '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
     | 'moon' '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
-    // colon‑prefixed API routes with optional full query strings
     | 'weather:' CITY ('?' search)?
     | 'forecast:' CITY ('?' search)?
     | 'location:' CITY ('?' search)?
+    | ':' 'weather' ':' CITY ('?' search)?   // new colon‑prefixed API route variant
     ;
 
 // helper token for language suffix used in PNG routes
 LANG_SUFFIX
-    : 'lang=' STRING
+    : ('lang=' STRING)
+    | STRING
     ;
 
 search
@@ -56,9 +56,9 @@
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // mixed flag chain with regular key=value pair
+    | 'use_imperial' ('=' DIGITS)?
+    | 'premium' ('=' DIGITS)?
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
-    // flag‑only chain allowing empty segments and repeated '&'
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))* )
     | 'lang' '=' STRING
     | 'format' '=' STRING
```
