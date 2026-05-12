# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 2 |
| From | run_20260511_202245Z_baseline_iteration_002 |
| To | run_20260511_202245Z_candidate_iteration_002 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | searchparameter, CITY, uri |

## Diff

```diff
--- run_20260511_202245Z_baseline_iteration_002
+++ run_20260511_202245Z_candidate_iteration_002
@@ -6,6 +6,8 @@
 
 uri
     : protocol '://' host ':' port '/' (':' )? query
+    // allow optional double slash before colon‑prefixed API routes or PNG paths
+    | protocol '://' host ':' port '//' (':' )? query
     ;
 
 protocol
@@ -60,6 +62,8 @@
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
     // flag‑only chain allowing empty segments and repeated '&'
     | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))* )
+    // pure flag‑only chain without any '='
+    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&' ('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+)* )
     | 'lang' '=' STRING
     | 'format' '=' STRING
     | 'location' '=' STRING
@@ -103,8 +107,8 @@
 
 CITY
     : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon'
-    // generic city allowing optional size, language suffix, trailing underscores and percent‑encoding
+    // generic city with optional size and language suffixes
     | [a-zA-Z]+ ('_' DIGITS 'x')? ('_'? 'lang=' (STRING | HEX))? ('_'*)?
-    // percent‑encoded city names like %E6%9C%AC%E5%9C%B0 (Tokyo in UTF‑8)
-    | (HEX)+
+    // percent‑encoded city optionally followed by size and language suffixes
+    | HEX ('_' DIGITS 'x')? ('_'? 'lang=' (STRING | HEX))?
     ;
```
