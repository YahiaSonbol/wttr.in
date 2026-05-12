# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 7 |
| From | run_20260511_195338Z_baseline_iteration_007 |
| To | run_20260511_195338Z_candidate_iteration_007 |
| Decision | promoted_to_champion |
| Mutation Status | accepted |
| Proposed Rules | CITY, searchparameter, query |

## Diff

```diff
--- run_20260511_195338Z_baseline_iteration_007
+++ run_20260511_195338Z_candidate_iteration_007
@@ -34,7 +34,10 @@
     | '?' 'format' '=' 'png'
     | 'moon' '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'moon' '@' CITY '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
-    // API‑style routes with optional full query strings
+    // new PNG routes with explicit size and language suffixes
+    | CITY '_'+ DIGITS 'x' '_lang=' STRING '.png'
+    | 'moon' '_' DIGITS 'x' '_lang=' STRING '.png'
+    // colon‑prefixed API routes with optional full query strings
     | 'weather:' CITY ('?' search)?
     | 'forecast:' CITY ('?' search)?
     | 'location:' CITY ('?' search)?
@@ -48,9 +51,10 @@
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // flag chains optionally mixed with other parameters
-    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))*)
-    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
+    // flag chains possibly mixed with key/value pairs in any order, allowing repeats
+    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))*
+       ('&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)*)
+    | (string ('=' (string | DIGITS | HEX | QUOTED_STRING))? '&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))
     | 'lang' '=' STRING
     | 'format' '=' STRING
     | 'location' '=' STRING
@@ -94,6 +98,6 @@
 
 CITY
     : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon'
-    // generic city, optional size suffix, mandatory language suffix for PNG routes, allow malformed suffixes
-    | [a-zA-Z]+ ('_' DIGITS 'x')? ('_lang=' STRING | '_lang=' HEX | '_lang=') 
+    // generic city with optional size and mandatory language suffix for PNG routes
+    | [a-zA-Z]+ ('_' DIGITS 'x')? '_lang=' (STRING | HEX)
     ;
```
