# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 2 |
| From | run_20260512_172431Z_baseline_iteration_002 |
| To | run_20260512_172431Z_candidate_iteration_002 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | query, searchparameter, uri |

## Diff

```diff
--- run_20260512_172431Z_baseline_iteration_002
+++ run_20260512_172431Z_candidate_iteration_002
@@ -6,10 +6,11 @@
 
 uri
     : protocol '://' host ':' port '/' query
-    // colon‑prefixed multi‑location API routes with optional period query
     | protocol '://' host ':' port '/' ('weather' | 'forecast' | 'location') ':' CITY ( ':' CITY )* ('?' 'period' '=' DIGITS)?
-    // special routes with /: prefix
     | protocol '://' host ':' port '/' ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source') ('?' search)?
+    | protocol '://' host ':' port '/' 'files' '/' STRING
+    | protocol '://' host ':' port '/' 'favicon.ico'
+    | protocol '://' host ':' port '/' 'malformed-response.html'
     ;
 
 protocol
@@ -41,19 +42,21 @@
     | 'moon' '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'moon' '@' CITY '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'moon' '@' STRING '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
-    // PNG routes with proper dimensions
     | CITY '_' DIGITS 'x' DIGITS '.png'
     | CITY '_' DIGITS 'x' '.png'
     | CITY '_' 'x' DIGITS '.png'
-    // extended PNG routes with variable size and language suffixes
     | CITY '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
     | 'moon' '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
-    // colon‑prefixed API routes with optional full query strings
     | 'weather:' CITY ('?' search)?
     | 'forecast:' CITY ('?' search)?
     | 'location:' CITY ('?' search)?
-    // use_imperial parameter
     | 'use_imperial' '=' ('true' | '1')
+    | 'debug' '=' 'true'
+    | 'narrow' '=' ('1' | 'true')
+    | '0'
+    | '1'
+    | '2'
+    | '3'
     ;
 
 // helper token for language suffix used in PNG routes
@@ -67,20 +70,19 @@
 
 searchparameter
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
-    | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
+    | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png' | '1' | '2' | '3' | '4' | '69' | STRING)
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // dedicated flag‑only bundle (e.g., FqT, AmdnF0)
     | FLAG_BUNDLE
-    // key=value pairs with flag bundles as value
     | string '=' FLAG_BUNDLE
     | 'lang' '=' STRING
     | 'format' '=' STRING
     | 'location' '=' STRING
     | 'city' '=' STRING
     | 'city' '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // use_imperial and narrow boolean parameters
     | 'use_imperial' '=' ('true' | '1')
     | 'narrow' '=' ('1' | 'true')
+    | 'background' '=' HEX
+    | 'transparency' '=' DIGITS
     ;
 
 FLAG_BUNDLE
```
