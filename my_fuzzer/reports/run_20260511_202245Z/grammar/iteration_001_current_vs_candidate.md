# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 1 |
| From | run_20260511_202245Z_baseline_iteration_001 |
| To | run_20260511_202245Z_candidate_iteration_001 |
| Decision | promoted_to_champion |
| Mutation Status | accepted |
| Proposed Rules | CITY, searchparameter, uri |

## Diff

```diff
--- run_20260511_202245Z_baseline_iteration_001
+++ run_20260511_202245Z_candidate_iteration_001
@@ -5,7 +5,7 @@
     ;
 
 uri
-    : protocol '://' host ':' port '/' query
+    : protocol '://' host ':' port '/' (':' )? query
     ;
 
 protocol
@@ -56,10 +56,10 @@
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // flag chains with possible empty segments and repeated '&' to test malformed queries
-    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))*)
+    // mixed flag chain with regular key=value pair
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
-    | string ('=' (string | DIGITS | HEX | QUOTED_STRING))? '&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+)
+    // flag‑only chain allowing empty segments and repeated '&'
+    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))* )
     | 'lang' '=' STRING
     | 'format' '=' STRING
     | 'location' '=' STRING
@@ -105,4 +105,6 @@
     : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon'
     // generic city allowing optional size, language suffix, trailing underscores and percent‑encoding
     | [a-zA-Z]+ ('_' DIGITS 'x')? ('_'? 'lang=' (STRING | HEX))? ('_'*)?
+    // percent‑encoded city names like %E6%9C%AC%E5%9C%B0 (Tokyo in UTF‑8)
+    | (HEX)+
     ;
```
