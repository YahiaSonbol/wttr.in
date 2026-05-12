# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 3 |
| From | run_20260512_172431Z_baseline_iteration_003 |
| To | run_20260512_172431Z_candidate_iteration_003 |
| Decision | kept_champion |
| Mutation Status | candidate_execution_error |
| Proposed Rules | query, searchparameter, uri |

## Diff

```diff
--- run_20260512_172431Z_baseline_iteration_003
+++ run_20260512_172431Z_candidate_iteration_003
@@ -10,6 +10,8 @@
     | protocol '://' host ':' port '/' ('weather' | 'forecast' | 'location') ':' CITY ( ':' CITY )* ('?' 'period' '=' DIGITS)?
     // special routes with /: prefix
     | protocol '://' host ':' port '/' ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source') ('?' search)?
+    // static file route for lib/wttr_srv.py:48
+    | protocol '://' host ':' port '/files/' STRING
     ;
 
 protocol
@@ -54,6 +56,9 @@
     | 'location:' CITY ('?' search)?
     // use_imperial parameter
     | 'use_imperial' '=' ('true' | '1')
+    // PNG rendering options for lib/fmt/png.py:96-105
+    | 'background' '=' HEX
+    | 'transparency' '=' DIGITS
     ;
 
 // helper token for language suffix used in PNG routes
@@ -68,6 +73,10 @@
 searchparameter
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
+    // numeric preconfigured format modes for lib/view/line.py
+    | 'format' '=' ('1' | '2' | '3' | '4' | '69')
+    // custom format placeholders: %l, %c, %t, %w, %m, %M, %S, %s, %D, %d, %z, %T, %Z
+    | 'format' '=' QUOTED_STRING
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
     // dedicated flag‑only bundle (e.g., FqT, AmdnF0)
     | FLAG_BUNDLE
@@ -81,6 +90,9 @@
     // use_imperial and narrow boolean parameters
     | 'use_imperial' '=' ('true' | '1')
     | 'narrow' '=' ('1' | 'true')
+    // PNG rendering options for lib/fmt/png.py:96-105
+    | 'background' '=' HEX
+    | 'transparency' '=' DIGITS
     ;
 
 FLAG_BUNDLE
```
