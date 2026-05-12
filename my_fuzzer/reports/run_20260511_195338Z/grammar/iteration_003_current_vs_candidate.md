# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 3 |
| From | run_20260511_195338Z_baseline_iteration_003 |
| To | run_20260511_195338Z_candidate_iteration_003 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | searchparameter, query, CITY |

## Diff

```diff
--- run_20260511_195338Z_baseline_iteration_003
+++ run_20260511_195338Z_candidate_iteration_003
@@ -34,10 +34,8 @@
     | '?' 'format' '=' 'png'
     | 'moon' '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'moon' '@' CITY '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
-    // API‑style routes with optional full query strings
-    | 'weather:' CITY ('?' search)?
-    | 'forecast:' CITY ('?' search)?
-    | 'location:' CITY ('?' search)?
+    // colon‑prefixed API routes with optional complex query strings
+    | '/'? ':'? ('weather' | 'forecast' | 'location') ':' CITY ('?' search)?
     ;
 
 search
@@ -48,8 +46,9 @@
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // flag chains optionally mixed with other parameters
-    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))*)
+    // flag chains optionally mixed with key‑value pairs, allow empty flag segments for deeper parsing
+    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))*
+       ( '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))? )* )
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
     | 'lang' '=' STRING
     | 'format' '=' STRING
@@ -94,6 +93,6 @@
 
 CITY
     : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon'
-    // generic city, optional size suffix, mandatory language suffix for PNG routes, allow malformed suffixes
-    | [a-zA-Z]+ ('_' DIGITS 'x')? ('_lang=' STRING | '_lang=' HEX | '_lang=') 
+    // generic city with optional PNG size and mandatory language suffix for PNG routes
+    | [a-zA-Z]+ ('_' DIGITS 'x')? ('_lang=' (STRING | HEX) )?
     ;
```
