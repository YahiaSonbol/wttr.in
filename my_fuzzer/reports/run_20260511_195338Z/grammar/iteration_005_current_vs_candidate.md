# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 5 |
| From | run_20260511_195338Z_baseline_iteration_005 |
| To | run_20260511_195338Z_candidate_iteration_005 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | query, searchparameter, CITY |

## Diff

```diff
--- run_20260511_195338Z_baseline_iteration_005
+++ run_20260511_195338Z_candidate_iteration_005
@@ -34,10 +34,11 @@
     | '?' 'format' '=' 'png'
     | 'moon' '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'moon' '@' CITY '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
-    // API‑style routes with optional full query strings
     | 'weather:' CITY ('?' search)?
     | 'forecast:' CITY ('?' search)?
     | 'location:' CITY ('?' search)?
+    // new moon PNG route with optional size and language suffixes
+    | 'moon' '@' CITY ('_' DIGITS 'x')? ('_lang=' (STRING|HEX)?)? '.png'
     ;
 
 search
@@ -49,8 +50,10 @@
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
     // flag chains optionally mixed with other parameters
-    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))*)
+    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))* )
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
+    // new mixed flag chain followed directly by a key/value pair (no extra '&')
+    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
     | 'lang' '=' STRING
     | 'format' '=' STRING
     | 'location' '=' STRING
@@ -94,6 +97,6 @@
 
 CITY
     : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon'
-    // generic city, optional size suffix, mandatory language suffix for PNG routes, allow malformed suffixes
-    | [a-zA-Z]+ ('_' DIGITS 'x')? ('_lang=' STRING | '_lang=' HEX | '_lang=') 
+    // generic city with optional size and language suffixes, allowing malformed or empty language parts and extra underscores
+    | [a-zA-Z]+ ('_' DIGITS 'x')? ('_lang=' (STRING|HEX)? )? ('_'*)
     ;
```
