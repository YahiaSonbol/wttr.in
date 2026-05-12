# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 1 |
| From | run_20260512_171416Z_baseline_iteration_001 |
| To | run_20260512_171416Z_candidate_iteration_001 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | searchparameter, uri, query |

## Diff

```diff
--- run_20260512_171416Z_baseline_iteration_001
+++ run_20260512_171416Z_candidate_iteration_001
@@ -6,8 +6,9 @@
 
 uri
     : protocol '://' host ':' port '/' (':' )? query
-    // colon‑prefixed multi‑location API routes with optional period query
     | protocol '://' host ':' port '/' (':' )? ('weather' | 'forecast' | 'location') ':' CITY ( ':' CITY )* ('?' 'period' '=' DIGITS)?
+    | '~' CITY
+    | IP_ADDR
     ;
 
 protocol
@@ -36,13 +37,13 @@
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
+    | ':' ('help' | 'translation' | 'bash.function' | 'iterm2')
+    | '?' 'debug' '=' ('true' | 'false')
     ;
 
 // helper token for language suffix used in PNG routes
@@ -56,17 +57,16 @@
 
 searchparameter
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
-    | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
-    | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // dedicated flag‑only bundle (e.g., FqT, AmdnF0)
+    | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png' | '%l:%c' | '%t' | '%w' | '%m' | '%M' | '%S' | '%s' | '%D' | '%d' | '%z' | '%T' | '%Z')
+    | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi' | STRING)
+    | 'use_imperial' '=' ('0' | '1')
+    | 'background' '=' HEX
+    | 'transparency' '=' DIGITS
+    | 'debug' '=' ('true' | 'false')
     | FLAG_BUNDLE
-    // key=value pairs with flag bundles as value
     | string '=' FLAG_BUNDLE
-    | 'lang' '=' STRING
-    | 'format' '=' STRING
     | 'location' '=' STRING
     | 'city' '=' STRING
-    | 'city' '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
     ;
 
 FLAG_BUNDLE
```
