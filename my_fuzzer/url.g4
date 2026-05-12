grammar url;

url
    : uri EOF
    ;

uri
    : BaseUrl '/' query
    // colon‑prefixed multi‑location API routes with optional period query
    | BaseUrl '/' ('weather' | 'forecast' | 'location') ':' CITY ( ':' CITY )* ('?' 'period' '=' DIGITS)?
    // special routes with /: prefix
    | BaseUrl '/' ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source') ('?' search)?
    ;

BaseUrl
    : 'wttr.in'
    ;

// protocol
//     : PROTOCOL
//     ;

// host
//     : HOSTNAME
//     ;

// port
//     : PORTS
//     ;

query
    : search
    | CITY
    | 'moon'
    | 'moon' '@' CITY
    | 'moon' '@' STRING
    | '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
    | '/' ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source') ('?' search)?
    | ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source') ('?' search)?
    | CITY '.png'
    | 'moon' '.png'
    | 'moon' '@' CITY '.png'
    | 'moon' '@' STRING '.png'
    | '?' 'format' '=' 'png'
    | 'moon' '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
    | 'moon' '@' CITY '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
    | 'moon' '@' STRING '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
    // PNG routes with proper dimensions
    | CITY '_' DIGITS 'x' DIGITS '.png'
    | CITY '_' DIGITS 'x' '.png'
    | CITY '_' 'x' DIGITS '.png'
    // extended PNG routes with variable size and language suffixes
    | CITY '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
    | 'moon' '_' DIGITS 'x' '_' LANG_SUFFIX ( '&' searchparameter )? '.png'
    // colon‑prefixed API routes with optional full query strings
    | 'weather:' CITY ('?' search)?
    | 'forecast:' CITY ('?' search)?
    | 'location:' CITY ('?' search)?
    // use_imperial parameter
    | 'use_imperial' '=' ('true' | '1')
    ;

// helper token for language suffix used in PNG routes
LANG_SUFFIX
    : 'lang=' STRING
    ;

search
    : searchparameter ('&' searchparameter)*
    ;

searchparameter
    : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
    | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
    | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
    // dedicated flag‑only bundle (e.g., FqT, AmdnF0)
    | FLAG_BUNDLE
    // key=value pairs with flag bundles as value
    | string '=' FLAG_BUNDLE
    | 'lang' '=' STRING
    | 'format' '=' STRING
    | 'location' '=' STRING
    | 'city' '=' STRING
    | 'city' '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
    // use_imperial and narrow boolean parameters
    | 'use_imperial' '=' ('true' | '1')
    | 'narrow' '=' ('1' | 'true')
    ;

FLAG_BUNDLE
    : ('A'|'d'|'n'|'m'|'M'|'u'|'I'|'t'|'T'|'p'|'q'|'Q'|'F'|'0'|'1'|'2'|'3')+
    ;

QUOTED_STRING
    : '\'' (~'\'' )* '\''
    ;

string
    : STRING
    | DIGITS
    ;

DIGITS
    : [0-9]+
    ;

HEX
    : ('%' [a-fA-F0-9] [a-fA-F0-9])+
    ;

STRING
    : ([a-zA-Z~0-9] | HEX) ([a-zA-Z0-9.+-] | HEX)*
    ;


PROTOCOL
    : 'http' 
    ;

HOSTNAME
    : 'localhost'
    ;

PORTS
    : '8002' 
    ;

CITY
    : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon'
    // generic city with optional size, language suffix and trailing underscores
    | [a-zA-Z]+ ('_' DIGITS 'x')? ('_'? 'lang=' (STRING | HEX))? ('_'*)?
    // percent‑encoded city names
    | (HEX)+
    // IPv4 address handling
    | IP_ADDR
    // tilde‑prefixed home location
    | TILDE_CITY
    // serialized payload locations prefixed with 'b_'
    | SERIAL_PAYLOAD
    ;

IP_ADDR
    : DIGITS '.' DIGITS '.' DIGITS '.' DIGITS
    ;

TILDE_CITY
    : '~' CITY
    ;

SERIAL_PAYLOAD
    : 'b_' (HEX | STRING)+
    ;
