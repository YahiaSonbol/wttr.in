# Grammar Diff Report

| Field | Value |
|---|---|
| Iteration | 7 |
| From | run_20260511_202245Z_baseline_iteration_007 |
| To | run_20260511_202245Z_candidate_iteration_007 |
| Decision | kept_champion |
| Mutation Status | regression |
| Proposed Rules | query, searchparameter, CITY |

## Diff

```diff
--- run_20260511_202245Z_baseline_iteration_007
+++ run_20260511_202245Z_candidate_iteration_007
@@ -21,26 +21,22 @@
     ;
 
 query
-    : search
-    | CITY
-    | 'moon'
-    | 'moon' '@' CITY
-    | '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
-    | '/' ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source') ('?' search)?
-    | ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source') ('?' search)?
+    : CITY                                 // plain weather page
+    | '/'?                                 // root default page
+    | '/' ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source') ('?' search)?   // colon‑prefixed help routes
+    | ':'? ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source') ('?' search)?               // slash‑less help routes
+    | 'weather:' CITY ('?' search)?
+    | 'forecast:' CITY ('?' search)?
+    | 'location:' CITY ('?' search)?
     | CITY '.png'
     | 'moon' '.png'
     | 'moon' '@' CITY '.png'
+    | '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | '?' 'format' '=' 'png'
     | 'moon' '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'moon' '@' CITY '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
-    // extended PNG routes with variable size and language suffixes, allowing optional flag chain after
     | CITY '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
     | 'moon' '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
-    // colon‑prefixed API routes with optional full query strings
-    | 'weather:' CITY ('?' search)?
-    | 'forecast:' CITY ('?' search)?
-    | 'location:' CITY ('?' search)?
     ;
 
 // helper token for language suffix used in PNG routes
@@ -56,10 +52,10 @@
     : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
     | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
     | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
-    // mixed flag chain with regular key=value pair
-    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))?)
-    // flag‑only chain allowing empty segments and repeated '&'
-    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&'*)? ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))* )
+    // mixed flag chain: one‑or‑more single‑letter flags optionally followed by a normal key=value pair
+    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ( '&' string ('=' (string | DIGITS | HEX | QUOTED_STRING))? )?)
+    // realistic flag‑only chain, limited to up to three flag groups
+    | (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+ ('&' (('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+))? )
     | 'lang' '=' STRING
     | 'format' '=' STRING
     | 'location' '=' STRING
@@ -103,8 +99,8 @@
 
 CITY
     : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon'
-    // generic city allowing optional size, language suffix, trailing underscores and percent‑encoding
-    | [a-zA-Z]+ ('_' DIGITS 'x')? ('_'? 'lang=' (STRING | HEX))? ('_'*)?
-    // percent‑encoded city names like %E6%9C%AC%E5%9C%B0 (Tokyo in UTF‑8)
+    // generic city: allow hyphens, plus‑encoded spaces, optional size, optional language suffix, optional trailing underscores
+    | [a-zA-Z]+ (('-'|'+')[a-zA-Z0-9]+)* ('_' DIGITS 'x')? ('_'? 'lang=' (STRING | HEX))? ('_'*)?
+    // percent‑encoded city names
     | (HEX)+
     ;
```
