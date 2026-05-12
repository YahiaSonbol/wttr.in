# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 3 |
| From | run_20260511_202245Z_baseline_iteration_003 |
| To | run_20260511_202245Z_candidate_iteration_003 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | searchparameter, CITY, query |

## Diff

```diff
--- run_20260511_202245Z_baseline_iteration_003
+++ run_20260511_202245Z_candidate_iteration_003
@@ -41,6 +41,8 @@
     | 'weather:' CITY ('?' search)?
     | 'forecast:' CITY ('?' search)?
     | 'location:' CITY ('?' search)?
+    // new moon PNG route with size, language and flag chain
+    | 'moon' '_' DIGITS 'x' '_' LANG_SUFFIX ('&' searchparameter)+
     ;
 
 // helper token for language suffix used in PNG routes
@@ -60,6 +62,8 @@
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
     // flag‑only chain allowing empty segments and repeated '&'
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))* )
+    // new production: multiple flag groups separated by '&' with optional trailing '&'
+    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))* '&'?)
     | 'lang' '=' STRING
     | 'format' '=' STRING
     | 'location' '=' STRING
@@ -103,8 +107,10 @@
 
 CITY
     : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon'
+    // explicit size and language suffix without .png
+    | [a-zA-Z]+ '_' DIGITS 'x' '_' 'lang=' STRING
     // generic city allowing optional size, language suffix, trailing underscores and percent‑encoding
     | [a-zA-Z]+ ('_' DIGITS 'x')? ('_'? 'lang=' (STRING | HEX))? ('_'*)?
-    // percent‑encoded city names like %E6%9C%AC%E5%9C%B0 (Tokyo in UTF‑8)
+    // percent‑encoded city names
     | (HEX)+
     ;
```
