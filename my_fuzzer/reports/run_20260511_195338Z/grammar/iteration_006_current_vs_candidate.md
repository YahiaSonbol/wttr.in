# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 6 |
| From | run_20260511_195338Z_baseline_iteration_006 |
| To | run_20260511_195338Z_candidate_iteration_006 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | CITY, searchparameter, query |

## Diff

```diff
--- run_20260511_195338Z_baseline_iteration_006
+++ run_20260511_195338Z_candidate_iteration_006
@@ -34,7 +34,9 @@
     | '?' 'format' '=' 'png'
     | 'moon' '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'moon' '@' CITY '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
-    // API‑style routes with optional full query strings
+    // new moon PNG routes with optional size and language suffixes
+    | 'moon' ( '_' DIGITS 'x' )? ( '_lang=' (STRING | HEX) )? '.png'
+    // API‑style routes with optional rich query strings
     | 'weather:' CITY ('?' search)?
     | 'forecast:' CITY ('?' search)?
     | 'location:' CITY ('?' search)?
@@ -46,10 +48,9 @@
 
 searchparameter
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
-    | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
-    | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // flag chains optionally mixed with other parameters
-    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))*)
+    | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png' | STRING) // allow malformed format values
+    | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi' | STRING) // allow arbitrary language strings
+    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))* )
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
     | 'lang' '=' STRING
     | 'format' '=' STRING
@@ -94,6 +95,6 @@
 
 CITY
     : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon'
-    // generic city, optional size suffix, mandatory language suffix for PNG routes, allow malformed suffixes
-    | [a-zA-Z]+ ('_' DIGITS 'x')? ('_lang=' STRING | '_lang=' HEX | '_lang=') 
+    // generic city with optional size and language suffixes for PNG routes
+    | [a-zA-Z]+ ( '_' DIGITS 'x' )? ( '_lang=' (STRING | HEX |) )?
     ;
```
