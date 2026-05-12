# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 8 |
| From | run_20260511_195338Z_baseline_iteration_008 |
| To | run_20260511_195338Z_candidate_iteration_008 |
| Decision | promoted_to_champion |
| Mutation Status | accepted |
| Proposed Rules | query, searchparameter, CITY |

## Diff

```diff
--- run_20260511_195338Z_baseline_iteration_008
+++ run_20260511_195338Z_candidate_iteration_008
@@ -34,13 +34,18 @@
     | '?' 'format' '=' 'png'
     | 'moon' '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'moon' '@' CITY '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
-    // new PNG routes with explicit size and language suffixes
-    | CITY '_'+ DIGITS 'x' '_lang=' STRING '.png'
-    | 'moon' '_' DIGITS 'x' '_lang=' STRING '.png'
+    // extended PNG routes with variable size and language suffixes, allowing optional flag chain after
+    | CITY '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
+    | 'moon' '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
     // colon‑prefixed API routes with optional full query strings
     | 'weather:' CITY ('?' search)?
     | 'forecast:' CITY ('?' search)?
     | 'location:' CITY ('?' search)?
+    ;
+
+// helper token for language suffix used in PNG routes
+LANG_SUFFIX
+    : 'lang=' STRING
     ;
 
 search
@@ -51,10 +56,10 @@
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // flag chains possibly mixed with key/value pairs in any order, allowing repeats
-    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))*
-       ('&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)*)
-    | (string ('=' (string | DIGITS | HEX | QUOTED_STRING))? '&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))
+    // flag chains with possible empty segments and repeated '&' to test malformed queries
+    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))*)
+    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
+    | string ('=' (string | DIGITS | HEX | QUOTED_STRING))? '&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+)
     | 'lang' '=' STRING
     | 'format' '=' STRING
     | 'location' '=' STRING
@@ -98,6 +103,6 @@
 
 CITY
     : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon'
-    // generic city with optional size and mandatory language suffix for PNG routes
-    | [a-zA-Z]+ ('_' DIGITS 'x')? '_lang=' (STRING | HEX)
+    // generic city allowing optional size, language suffix, trailing underscores and percent‑encoding
+    | [a-zA-Z]+ ('_' DIGITS 'x')? ('_'? 'lang=' (STRING | HEX))? ('_'*)?
     ;
```
