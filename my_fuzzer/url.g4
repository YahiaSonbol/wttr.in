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
    : CITY
    | CITY '.png'
    | CITY '?' search
    | CITY '.png' '?' search
    ;

search
    : searchparameter
    ;

searchparameter
    : 'format' '=' ('j1' | 'j2' | 'p1' | 'v2' | 'v2d' | 'v2n')
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
    : 'cairo' | 'paris' | 'london' | 'tokyo' | 'berlin' | 'madrid' | 'dubai' | 'singapore' | 'bangkok' | 'beijing' | 'sydney' | 'newyork' | 'losangeles' | 'rome' | 'moscow' | 'seoul' | 'new-york' | 'los-angeles' | 'delhi' | 'hongkong' | 'istanbul' | 'riyadh' | 'toronto'
    ;
