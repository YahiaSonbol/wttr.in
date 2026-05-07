grammar url;

url
    : uri EOF
    ;

uri
    : protocol '://' host ':' port '/' query
    ;

protocol
    : PROTOCOL
    ;

host
    : HOSTNAME
    ;

port
    : PORTS
    ;

query
    : search
    | CITY
    | 'moon'
    | 'moon' '@' CITY
    | '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
    | '/' ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source')
    // expose special routes without leading slash
    | ':' ('help' | 'translation' | 'bash.function' | 'iterm2' | 'health' | 'metrics' | 'config' | 'source')
    | CITY '.png'
    | 'moon' '.png'
    | 'moon' '@' CITY '.png'
    | '?' 'format' '=' 'png'
    | 'moon' '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
    | 'moon' '@' CITY '?' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
    | 'moon' '?' 'lang' '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
    | 'moon' '@' CITY '?' 'lang' '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
    | 'moon' '?' 'lang' '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi') '&' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
    | 'moon' '@' CITY '?' 'lang' '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi') '&' 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
    | CITY '?' search
    | CITY '.png' '?' search
    | 'moon' '@' CITY '?' search
    | 'moon' '?' 'lang' '=' STRING '&' 'format' '=' STRING
    | 'moon' '@' CITY '?' 'lang' '=' STRING '&' 'format' '=' STRING
    | CITY '_200x_lang=' STRING '.png'
    | 'moon' '@' CITY '_200x_lang=' STRING '.png'
    | CITY '_200x_lang=' STRING '?' search
    | 'moon' '@' CITY '?' searchparameter ('&' searchparameter)*
    // prefixed API style routes
    | 'weather' ':' CITY
    | 'forecast' ':' CITY
    | 'location' ':' CITY
    ;

search
    : searchparameter ('&' searchparameter)*
    ;

searchparameter
    : string ('=' (string | DIGITS | HEX | QUOTED_STRING))?
    | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
    | 'lang'   '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
    | 'A' | 'd' | 'n' | 'm' | 'M' | 'u' | 'I' | 't' | 'T' | 'p' | 'q' | 'Q' | 'F' | '0' | '1' | '2' | '3'
    | 'lang' '=' STRING
    | 'format' '=' STRING
    | 'location' '=' STRING
    | 'city' '=' STRING
    | 'city' '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
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
    // generic city, optional size (e.g., city_200x) and mandatory language code suffix for PNG paths
    | [a-zA-Z]+ ('_' [0-9]+ 'x')? '_lang=' STRING
    ;
