/*
BSD License

Copyright (c) 2016, Tom Everett
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. Neither the name of Tom Everett nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

/**
* scheme:[//[user:password@]host[:port]][/]path[?query][#fragment]
*/

// $antlr-format alignTrailingComments true, columnLimit 150, minEmptyLines 1, maxEmptyLinesToKeep 1, reflowComments false, useTab false
// $antlr-format allowShortRulesOnASingleLine false, allowShortBlocksOnASingleLine true, alignSemicolons hanging, alignColons hanging

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
    | '/' ':' ('help' | 'translation' | 'bash.function' | 'iterm2')
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
    ;

search
    : searchparameter ('&' searchparameter)*
    ;

searchparameter
    : string ('=' (string | DIGITS | HEX))?
    | 'format' '=' ('j1' | 'j2' | 'v2' | 'v2n' | 'v2d' | 'p1' | 'png')
    | 'lang' '=' ('en' | 'ru' | 'de' | 'es' | 'fr' | 'ja' | 'zh' | 'ko' | 'ar' | 'th' | 'tr' | 'hi')
    | 'A' | 'd' | 'n' | 'm' | 'M' | 'u' | 'I' | 't' | 'T' | 'p' | 'q' | 'Q' | 'F' | '0' | '1' | '2' | '3'
    | 'lang' '=' STRING
    | 'format' '=' STRING
    | 'location' '=' STRING
    | 'city' '=' STRING
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
    : 'cairo' | 'paris' | 'london' | 'newyork' | 'tokyo' | 'moscow' | 'beijing' | 'delhi' | 'sydney' | 'rome' | 'berlin' | 'madrid' | 'toronto' | 'dubai' | 'singapore' | 'hongkong' | 'seoul' | 'bangkok' | 'istanbul' | 'riyadh' | 'moon' | 'Paris_200x_lang=ru' | 'London_200x_lang=en' | 'Tokyo_200x_lang=jp' | 'NewYork_200x_lang=en' | 'Berlin_200x_lang=de' | 'moscow_200x_lang=ru' | 'beijing_200x_lang=zh' | 'delhi_200x_lang=hi' | 'sydney_200x_lang=en' | 'rome_200x_lang=it' | 'madrid_200x_lang=es' | 'toronto_200x_lang=en' | 'dubai_200x_lang=ar' | 'singapore_200x_lang=en' | 'hongkong_200x_lang=zh' | 'seoul_200x_lang=ko' | 'bangkok_200x_lang=th' | 'istanbul_200x_lang=tr' | 'riyadh_200x_lang=ar'
    ;
