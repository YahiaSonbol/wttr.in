# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 2 |
| From | run_20260512_172431Z_baseline_iteration_001 |
| To | run_20260512_172431Z_baseline_iteration_002 |
| Decision | baseline_comparison |
| Mutation Status | baseline |
| Baseline Reference | run_20260512_172431Z_baseline_iteration_001 |

## Diff

```diff
--- run_20260512_172431Z_baseline_iteration_001
+++ run_20260512_172431Z_baseline_iteration_002
@@ -5,9 +5,11 @@
     ;
 
 uri
-    : protocol '://' host ':' port '/' (':' )? query
+    : protocol '://' host ':' port '/' query
     // colon‑prefixed multi‑location API routes with optional period query
-    | protocol '://' host ':' port '/' (':' )? ('weather' | 'forecast' | 'location') ':' CITY ( ':' CITY )* ('?' 'period' '=' DIGITS)?
+    | protocol '://' host ':' port '/' ('weather' | 'forecast' | 'location') ':' CITY ( ':' CITY )* ('?' 'period' '=' DIGITS)?
+    // special routes with /: prefix
+    | protocol '://' host ':' port '/' ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source') ('?' search)?
     ;
 
 protocol
@@ -27,22 +29,31 @@
     | CITY
     | 'moon'
     | 'moon' '@' CITY
+    | 'moon' '@' STRING
     | '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | '/' ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source') ('?' search)?
     | ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source') ('?' search)?
     | CITY '.png'
     | 'moon' '.png'
     | 'moon' '@' CITY '.png'
+    | 'moon' '@' STRING '.png'
     | '?' 'format' '=' 'png'
     | 'moon' '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'moon' '@' CITY '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
-    // extended PNG routes with variable size and language suffixes, allowing optional flag chain after
+    | 'moon' '@' STRING '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
+    // PNG routes with proper dimensions
+    | CITY '_' DIGITS 'x' DIGITS '.png'
+    | CITY '_' DIGITS 'x' '.png'
+    | CITY '_' 'x' DIGITS '.png'
+    // extended PNG routes with variable size and language suffixes
     | CITY '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
     | 'moon' '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
     // colon‑prefixed API routes with optional full query strings
     | 'weather:' CITY ('?' search)?
     | 'forecast:' CITY ('?' search)?
     | 'location:' CITY ('?' search)?
+    // use_imperial parameter
+    | 'use_imperial' '=' ('true' | '1')
     ;
 
 // helper token for language suffix used in PNG routes
@@ -67,6 +78,9 @@
     | 'location' '=' STRING
     | 'city' '=' STRING
     | 'city' '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
+    // use_imperial and narrow boolean parameters
+    | 'use_imperial' '=' ('true' | '1')
+    | 'narrow' '=' ('1' | 'true')
     ;
 
 FLAG_BUNDLE
```
