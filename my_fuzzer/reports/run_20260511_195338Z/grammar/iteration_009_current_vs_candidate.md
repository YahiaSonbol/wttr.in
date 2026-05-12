# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 9 |
| From | run_20260511_195338Z_baseline_iteration_009 |
| To | run_20260511_195338Z_candidate_iteration_009 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | searchparameter, query, CITY |

## Diff

```diff
--- run_20260511_195338Z_baseline_iteration_009
+++ run_20260511_195338Z_candidate_iteration_009
@@ -34,13 +34,16 @@
     | '?' 'format' '=' 'png'
     | 'moon' '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'moon' '@' CITY '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
-    // extended PNG routes with variable size and language suffixes, allowing optional flag chain after
+    // extended PNG routes with variable size, language suffixes and flag chains
     | CITY '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
     | 'moon' '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
-    // colon‑prefixed API routes with optional full query strings
+    // colon‑prefixed API routes with full query strings and flag chains
     | 'weather:' CITY ('?' search)?
     | 'forecast:' CITY ('?' search)?
     | 'location:' CITY ('?' search)?
+    // moon routes with additional parameters beyond format
+    | 'moon' '?' search
+    | 'moon' '@' CITY '?' search
     ;
 
 // helper token for language suffix used in PNG routes
@@ -56,8 +59,8 @@
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // flag chains with possible empty segments and repeated '&' to test malformed queries
-    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))*)
+    // mixed flag/key‑value chains, allowing empty segments and repeated '&'
+    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))* )
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
     | string ('=' (string | DIGITS | HEX | QUOTED_STRING))? '&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+)
     | 'lang' '=' STRING
@@ -103,6 +106,6 @@
 
 CITY
     : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon'
-    // generic city allowing optional size, language suffix, trailing underscores and percent‑encoding
-    | [a-zA-Z]+ ('_' DIGITS 'x')? ('_'? 'lang=' (STRING | HEX))? ('_'*)?
+    // generic city allowing multiple size/lang segments, percent‑encoding and trailing underscores
+    | [a-zA-Z]+ ( '_' DIGITS 'x' )? ( '_'? 'lang=' (STRING | HEX) )? ( '_' (DIGITS 'x')? )* '_'*
     ;
```
