# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 6 |
| From | run_20260511_202245Z_baseline_iteration_006 |
| To | run_20260511_202245Z_candidate_iteration_006 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | searchparameter, query, CITY |

## Diff

```diff
--- run_20260511_202245Z_baseline_iteration_006
+++ run_20260511_202245Z_candidate_iteration_006
@@ -41,6 +41,8 @@
     | 'weather:' CITY ('?' search)?
     | 'forecast:' CITY ('?' search)?
     | 'location:' CITY ('?' search)?
+    // explicit help/translation routes with format and language parameters
+    | ':' ('help' | 'translation' | 'bash.function' | 'iterm2') '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png') '&' 'lang' '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
     ;
 
 // helper token for language suffix used in PNG routes
@@ -56,9 +58,9 @@
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // mixed flag chain with regular key=value pair
+    // mixed flag chain followed by optional key=value pair
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
-    // flag‑only chain allowing empty segments and repeated '&'
+    // flag‑only chain allowing repeated '&' and optional empty segments
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))* )
     | 'lang' '=' STRING
     | 'format' '=' STRING
@@ -103,8 +105,8 @@
 
 CITY
     : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon'
-    // generic city allowing optional size, language suffix, trailing underscores and percent‑encoding
-    | [a-zA-Z]+ ('_' DIGITS 'x')? ('_'? 'lang=' (STRING | HEX))? ('_'*)?
-    // percent‑encoded city names like %E6%9C%AC%E5%9C%B0 (Tokyo in UTF‑8)
-    | (HEX)+
+    // generic city allowing multiple optional '_' segments for size, language and extra underscores
+    | [a-zA-Z]+ ( '_' DIGITS 'x' )? ( '_'? 'lang=' (STRING | HEX) )? ( '_'* )?
+    // percent‑encoded city names, allowing one or more HEX groups optionally followed by size/lang suffixes
+    | (HEX)+ ( '_' DIGITS 'x' )? ( '_'? 'lang=' (STRING | HEX) )? ( '_'* )?
     ;
```
