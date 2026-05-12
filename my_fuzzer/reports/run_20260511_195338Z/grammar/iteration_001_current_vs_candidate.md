# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 1 |
| From | run_20260511_195338Z_baseline_iteration_001 |
| To | run_20260511_195338Z_candidate_iteration_001 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | CITY, searchparameter, query |

## Diff

```diff
--- run_20260511_195338Z_baseline_iteration_001
+++ run_20260511_195338Z_candidate_iteration_001
@@ -38,6 +38,8 @@
     | 'weather:' CITY ('?' search)?
     | 'forecast:' CITY ('?' search)?
     | 'location:' CITY ('?' search)?
+    // colon‑prefixed routes with optional trailing slash and optional query string
+    | '/' ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source') '/'? ('?' search)?
     ;
 
 search
@@ -48,8 +50,9 @@
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // allow arbitrary flag chains mixed with other parameters
+    // flag chains possibly mixed with other parameters
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))*)
+    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' (string ('=' (string | DIGITS | HEX | QUOTED_STRING))?))
     | 'lang' '=' STRING
     | 'format' '=' STRING
     | 'location' '=' STRING
@@ -93,6 +96,6 @@
 
 CITY
     : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon'
-    // generic city with optional size and mandatory language suffix for PNG routes
+    // generic city with optional size (e.g., _200x) and mandatory language suffix for PNG routes; allow uppercase letters
     | [a-zA-Z]+ ('_' DIGITS 'x')? '_lang=' STRING
     ;
```
