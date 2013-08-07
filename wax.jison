%lex
%%

\s+                   /* nil */

'['                   return 'INDENT'; // TODO: lexer tracks indent stack
']'                   return 'DEDENT'; // TODO
[a-zA-Z0-9:${}]+         return 'WORD';
["']                  return 'QUOTE';
//';'                   return ';' // TODO colon ambiguity if allowed in WORD
'.'                   return '.';
'#'                   return '#';
'|'                   return '|';
<<EOF>>               return 'EOF';

/lex

%%

DOCUMENT:
  NODES EOF{ return $1; }
  ;

NODES:
  NODES NODE { $$ = $1 + $2 + '<br/>'; }
  | NODE { $$ = $1 + '<br/>'; }
  ;

NODE:
  NAME INDENT NODES DEDENT { $$ = '&lt;'+$1+'>' + $3 + '&lt;/'+$1+'>';}
  | NAME { $$ = '&lt;'+$1+'/>'; }
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
  ATNAME ATVAL { $$ = ' ' + $1 + '=' + $2; }
  ;

ATNAME:
  WORD { $$ = $1; }
  ;

ATVAL:
  QUOTE WORDS QUOTE { $$ = $2; }
  |WORD { $$ = $1; }
  ;

WORDS:
  WORDS WORD { $$ = $1 + ' ' + $2; }
  | WORD { $$ = $1; }
  ;