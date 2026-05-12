# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 5 |
| From | run_20260511_202245Z_baseline_iteration_005 |
| To | run_20260511_202245Z_candidate_iteration_005 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | searchparameter, CITY, query |

## Diff

```diff
--- run_20260511_202245Z_baseline_iteration_005
+++ run_20260511_202245Z_candidate_iteration_005
@@ -34,13 +34,11 @@
     | '?' 'format' '=' 'png'
     | 'moon' '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'moon' '@' CITY '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
-    // extended PNG routes with variable size and language suffixes, allowing optional flag chain after
+    // extended PNG routes with size, language and optional flag chain
     | CITY '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
     | 'moon' '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
-    // colon‑prefixed API routes with optional full query strings
-    | 'weather:' CITY ('?' search)?
-    | 'forecast:' CITY ('?' search)?
-    | 'location:' CITY ('?' search)?
+    // colon‑prefixed API routes with full query strings
+    | ':' ('weather' | 'forecast' | 'location') ':' CITY ('?' search)?
     ;
 
 // helper token for language suffix used in PNG routes
@@ -56,12 +54,14 @@
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
+    // explicit size flag for PNG validation
+    | 'size'   '=' DIGITS
+    // language flag chain followed by optional flag‑only segments
+    | 'lang'   '=' STRING ('&' ('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ )*
     // mixed flag chain with regular key=value pair
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
     // flag‑only chain allowing empty segments and repeated '&'
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))* )
-    | 'lang' '=' STRING
-    | 'format' '=' STRING
     | 'location' '=' STRING
     | 'city' '=' STRING
     | 'city' '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
@@ -103,8 +103,8 @@
 
 CITY
     : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon'
-    // generic city allowing optional size, language suffix, trailing underscores and percent‑encoding
-    | [a-zA-Z]+ ('_' DIGITS 'x')? ('_'? 'lang=' (STRING | HEX))? ('_'*)?
-    // percent‑encoded city names like %E6%9C%AC%E5%9C%B0 (Tokyo in UTF‑8)
+    // deterministic multi‑segment pattern for PNG routes
+    | [a-zA-Z]+ ('_' DIGITS 'x')? ('_' 'lang=' STRING)? ('_' DIGITS 'x')* ('_'*)?
+    // percent‑encoded city names
     | (HEX)+
     ;
```
