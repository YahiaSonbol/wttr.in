# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 2 |
| From | run_20260512_155702Z_baseline_iteration_002 |
| To | run_20260512_155702Z_candidate_iteration_002 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | searchparameter, uri, search |

## Diff

```diff
--- run_20260512_155702Z_baseline_iteration_002
+++ run_20260512_155702Z_candidate_iteration_002
@@ -6,6 +6,9 @@
 
 uri
     : protocol '://' host ':' port '/' (':' )? query
+    // explicit PNG routes with mandatory size token and language suffix
+    | protocol '://' host ':' port '/' CITY '_' DIGITS 'x' '_' LANG_SUFFIX '.png'
+    | protocol '://' host ':' port '/' 'moon' '_' DIGITS 'x' '_' LANG_SUFFIX '.png'
     ;
 
 protocol
@@ -56,15 +59,9 @@
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // mixed flag chain with regular key=value pair
-    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
-    // flag‑only chain allowing empty segments and repeated '&'
-    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))* )
-    | 'lang' '=' STRING
-    | 'format' '=' STRING
-    | 'location' '=' STRING
-    | 'city' '=' STRING
-    | 'city' '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
+    | 'use_imperial' '=' ('true' | 'false' | '1' | '0')
+    // flag‑only chain, allowing repeated '&' and mixed flag/value segments
+    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('=' (string | DIGITS | HEX | QUOTED_STRING))?))*)
     ;
 
 QUOTED_STRING
```
