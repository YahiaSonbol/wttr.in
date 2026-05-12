# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 2 |
| From | run_20260512_163233Z_baseline_iteration_002 |
| To | run_20260512_163233Z_candidate_iteration_002 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | FLAG_BUNDLE, searchparameter, uri |

## Diff

```diff
--- run_20260512_163233Z_baseline_iteration_002
+++ run_20260512_163233Z_candidate_iteration_002
@@ -8,6 +8,8 @@
     : protocol '://' host ':' port '/' (':' )? query
     // colon‑prefixed multi‑location API routes with optional period query
     | protocol '://' host ':' port '/' (':' )? ('weather' | 'forecast' | 'location') ':' CITY ( ':' CITY )* ('?' 'period' '=' DIGITS)?
+    // direct location paths including tilde, IP, and serialized payloads
+    | protocol '://' host ':' port '/' (':' )? (CITY | TILDE_CITY | IP_ADDR | SERIAL_PAYLOAD) ( '?' search )?
     ;
 
 protocol
@@ -57,16 +59,12 @@
 searchparameter
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
-    | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // dedicated flag‑only bundle (e.g., FqT, AmdnF0)
+    | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi' | STRING)
+    | 'use_imperial' '=' DIGITS
+    | 'background' '=' HEX
+    | 'transparency' '=' DIGITS
     | FLAG_BUNDLE
-    // key=value pairs with flag bundles as value
     | string '=' FLAG_BUNDLE
-    | 'lang' '=' STRING
-    | 'format' '=' STRING
-    | 'location' '=' STRING
-    | 'city' '=' STRING
-    | 'city' '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
     ;
 
 FLAG_BUNDLE
```
