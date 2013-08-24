%lex
%%

\s+                     /* nil */
'['                     return 'INDENT'; // TODO: lexer tracks indent stack
']'                     return 'DEDENT'; // TODO
[a-zA-Z0-9:${}]+        return 'WORD';
["']                    return 'QUOTE';
//';'                   return ';' // TODO colon ambiguity if allowed in WORD
'.'                     return '.';
'#'                     return '#';
'|'                     return '|';
'!'                     return '!';
<<EOF>>                 return 'EOF';

/lex

%%

DOCUMENT:
    PROLOG ELEMENTS EOF{ return $1 + $2; }
    | ELEMENTS EOF { console.log($1); return $1; }
    ;

PROLOG:
    '!' WORD { $$ = $2;}
    ;

ELEMENTS:
    ELEMENTS ELEMENT { $$ = $1 + $2; }
    | ELEMENT { $$ = $1; }
    ;

ELEMENT:
    NAME INDENT ELEMENTS DEDENT { $$ = '<'+$1+'>' + $3 + '</'+$1+'>';}
    | NAME { $$ = '<'+$1+'/>'; }
    | TEXT { $$ = $1; }
    ;

TEXT:
    QUOTE WORDS QUOTE { $$ = $2; }
    ;

NAME:
    NAME '.' WORD { $$ = $1 + ' class=\'' + $3 + '\''; }
    | NAME '#' WORD { $$ = $1 + ' id=' + $3; }
    | NAME '|' ATTR { $$ = $1 + $3; }
    | WORD { $$ = $1; }
    ;

ATTR:
    ATTRNAME ATTRVAL { $$ = ' ' + $1 + '=' + $2; }
    ;

ATTRNAME:
    WORD { $$ = $1; }
    ;

ATTRVAL:
    QUOTE WORDS QUOTE { $$ = $2; }
    |WORD { $$ = $1; }
    ;

WORDS:
    WORDS WORD { $$ = $1 + ' ' + $2; }
    | WORD { $$ = $1; }
    ;
