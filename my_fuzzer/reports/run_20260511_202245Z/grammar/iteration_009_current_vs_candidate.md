# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 9 |
| From | run_20260511_202245Z_baseline_iteration_009 |
| To | run_20260511_202245Z_candidate_iteration_009 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | CITY, searchparameter, query |

## Diff

```diff
--- run_20260511_202245Z_baseline_iteration_009
+++ run_20260511_202245Z_candidate_iteration_009
@@ -37,6 +37,8 @@
     // extended PNG routes with variable size and language suffixes, allowing optional flag chain after
     | CITY '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
     | 'moon' '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
+    // moon routes with size, language and format flags
+    | 'moon' '@' CITY '_' DIGITS 'x' '_' LANG_SUFFIX '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     // colon‑prefixed API routes with optional full query strings
     | 'weather:' CITY ('?' search)?
     | 'forecast:' CITY ('?' search)?
@@ -58,7 +60,7 @@
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
     // mixed flag chain with regular key=value pair
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
-    // flag‑only chain allowing empty segments and repeated '&'
+    // flag‑only chain, allowing empty segments, repeated '&', and trailing '&'
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))* )
     | 'lang' '=' STRING
     | 'format' '=' STRING
@@ -103,8 +105,8 @@
 
 CITY
     : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon'
-    // generic city allowing optional size, language suffix, trailing underscores and percent‑encoding
-    | [a-zA-Z]+ ('_' DIGITS 'x')? ('_'? 'lang=' (STRING | HEX))? ('_'*)?
-    // percent‑encoded city names like %E6%9C%AC%E5%9C%B0 (Tokyo in UTF‑8)
+    // generic city allowing multiple size and language segments, optional trailing underscores, and percent‑encoding
+    | [a-zA-Z]+ ( '_' DIGITS 'x' )* ( '_'? 'lang=' (STRING | HEX) )* ('_'*)?
+    // percent‑encoded city names
     | (HEX)+
     ;
```
