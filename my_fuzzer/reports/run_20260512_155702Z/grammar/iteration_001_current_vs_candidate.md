# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 1 |
| From | run_20260512_155702Z_baseline_iteration_001 |
| To | run_20260512_155702Z_candidate_iteration_001 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | searchparameter, query, uri |

## Diff

```diff
--- run_20260512_155702Z_baseline_iteration_001
+++ run_20260512_155702Z_candidate_iteration_001
@@ -5,7 +5,7 @@
     ;
 
 uri
-    : protocol '://' host ':' port '/' (':' )? query
+    : protocol '://' host ':' port '/' (':' )? ( CITY '_' DIGITS 'x' '_' LANG_SUFFIX '.png' | query )
     ;
 
 protocol
@@ -34,13 +34,12 @@
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
+    | ':' ('weather' | 'forecast' | 'location') ('?' search)?
     ;
 
 // helper token for language suffix used in PNG routes
@@ -56,9 +55,8 @@
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // mixed flag chain with regular key=value pair
+    | 'use_imperial' ('=' (string | DIGITS))?
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
-    // flag‑only chain allowing empty segments and repeated '&'
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))* )
     | 'lang' '=' STRING
     | 'format' '=' STRING
```
