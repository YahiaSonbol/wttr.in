# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 3 |
| From | run_20260511_195338Z_baseline_iteration_002 |
| To | run_20260511_195338Z_baseline_iteration_003 |
| Decision | baseline_comparison |
| Mutation Status | baseline |
| Baseline Reference | run_20260511_195338Z_baseline_iteration_002 |

## Diff

```diff
--- run_20260511_195338Z_baseline_iteration_002
+++ run_20260511_195338Z_baseline_iteration_003
@@ -26,8 +26,8 @@
     | 'moon'
     | 'moon' '@' CITY
     | '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
-    | '/' ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source')
-    | ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source')
+    | '/' ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source') ('?' search)?
+    | ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source') ('?' search)?
     | CITY '.png'
     | 'moon' '.png'
     | 'moon' '@' CITY '.png'
@@ -48,8 +48,9 @@
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // allow arbitrary flag chains mixed with other parameters
+    // flag chains optionally mixed with other parameters
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))*)
+    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
     | 'lang' '=' STRING
     | 'format' '=' STRING
     | 'location' '=' STRING
@@ -93,6 +94,6 @@
 
 CITY
     : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon'
-    // generic city with optional size and mandatory language suffix for PNG routes
-    | [a-zA-Z]+ ('_' DIGITS 'x')? '_lang=' STRING
+    // generic city, optional size suffix, mandatory language suffix for PNG routes, allow malformed suffixes
+    | [a-zA-Z]+ ('_' DIGITS 'x')? ('_lang=' STRING | '_lang=' HEX | '_lang=') 
     ;
```
