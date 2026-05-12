# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 1 |
| From | run_20260512_163233Z_baseline_iteration_001 |
| To | run_20260512_163233Z_candidate_iteration_001 |
| Decision | promoted_to_champion |
| Mutation Status | accepted |
| Proposed Rules | searchparameter, CITY, uri |

## Diff

```diff
--- run_20260512_163233Z_baseline_iteration_001
+++ run_20260512_163233Z_candidate_iteration_001
@@ -6,6 +6,8 @@
 
 uri
     : protocol '://' host ':' port '/' (':' )? query
+    // colon‑prefixed multi‑location API routes with optional period query
+    | protocol '://' host ':' port '/' (':' )? ('weather' | 'forecast' | 'location') ':' CITY ( ':' CITY )* ('?' 'period' '=' DIGITS)?
     ;
 
 protocol
@@ -56,15 +58,19 @@
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // mixed flag chain with regular key=value pair
-    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
-    // flag‑only chain allowing empty segments and repeated '&'
-    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))* )
+    // dedicated flag‑only bundle (e.g., FqT, AmdnF0)
+    | FLAG_BUNDLE
+    // key=value pairs with flag bundles as value
+    | string '=' FLAG_BUNDLE
     | 'lang' '=' STRING
     | 'format' '=' STRING
     | 'location' '=' STRING
     | 'city' '=' STRING
     | 'city' '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
+    ;
+
+FLAG_BUNDLE
+    : ('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+
     ;
 
 QUOTED_STRING
@@ -103,8 +109,26 @@
 
 CITY
     : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon'
-    // generic city allowing optional size, language suffix, trailing underscores and percent‑encoding
+    // generic city with optional size, language suffix and trailing underscores
     | [a-zA-Z]+ ('_' DIGITS 'x')? ('_'? 'lang=' (STRING | HEX))? ('_'*)?
-    // percent‑encoded city names like %E6%9C%AC%E5%9C%B0 (Tokyo in UTF‑8)
+    // percent‑encoded city names
     | (HEX)+
+    // IPv4 address handling
+    | IP_ADDR
+    // tilde‑prefixed home location
+    | TILDE_CITY
+    // serialized payload locations prefixed with 'b_'
+    | SERIAL_PAYLOAD
     ;
+
+IP_ADDR
+    : DIGITS '.' DIGITS '.' DIGITS '.' DIGITS
+    ;
+
+TILDE_CITY
+    : '~' CITY
+    ;
+
+SERIAL_PAYLOAD
+    : 'b_' (HEX | STRING)+
+    ;
```
