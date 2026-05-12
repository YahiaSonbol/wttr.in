# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 1 |
| From | run_20260512_175320Z_baseline_iteration_001 |
| To | run_20260512_175320Z_candidate_iteration_001 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | searchparameter, uri, search |

## Diff

```diff
--- run_20260512_175320Z_baseline_iteration_001
+++ run_20260512_175320Z_candidate_iteration_001
@@ -10,6 +10,14 @@
     | protocol '://' host ':' port '/' ('weather' | 'forecast' | 'location') ':' CITY ( ':' CITY )* ('?' 'period' '=' DIGITS)?
     // special routes with /: prefix
     | protocol '://' host ':' port '/' ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source') ('?' search)?
+    // multi‑location cycling via path separators
+    | protocol '://' host ':' port '/' CITY ( ':' CITY )+ ('?' search)?
+    // IP address as location path
+    | protocol '://' host ':' port '/' IP_ADDR
+    // tilde‑prefixed home location
+    | protocol '://' host ':' port '/' TILDE_CITY
+    // serialized payload location
+    | protocol '://' host ':' port '/' SERIAL_PAYLOAD
     ;
 
 protocol
@@ -63,24 +71,25 @@
 
 search
     : searchparameter ('&' searchparameter)*
+    | FLAG_BUNDLE ('&' FLAG_BUNDLE)*
     ;
 
 searchparameter
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
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
+    | 'debug' '=' ('true' | '1')
+    | 'background' '=' HEX
+    | 'transparency' '=' DIGITS
     ;
 
 FLAG_BUNDLE
```
