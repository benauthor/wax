/*globals console: false, process: false */
var fs = require('fs'),
    Parser = require("jison").Parser,
    Lexer = require("lex");

// load grammar from wax.json
var wax = JSON.parse(fs.readFileSync("wax.json"));
console.log(wax);

var grammar = {"bnf": wax},
    parser = new Parser(grammar),
    lexer = parser.lexer = new Lexer();

// lexer rules
/*
\s+                     //
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
*/
lexer.addRule(/\s+/, function () {}); // this will change for significant whitespace
lexer.addRule(/\[/, function () { return 'INDENT'; }); // ditto
lexer.addRule(/\]/, function () { return 'DEDENT'; }); // ditto
lexer.addRule(/[a-zA-Z0-9:${}]+/, function (lexeme) {
    this.yytext = lexeme;
    return "WORD";
});
lexer.addRule(/['"]/, function () { return 'QUOTE'; });
lexer.addRule(/\./, function () { return '.'; });
lexer.addRule(/;/, function () { return ';'; });
lexer.addRule(/#/, function () { return '#'; });
lexer.addRule(/\|/, function () { return '|'; });
lexer.addRule(/!/, function () { return '!'; });
lexer.addRule(/$/, function () { return "EOF"; });


// parse a file
fs.readFile(process.argv[2], 'utf8', function (err,data) {
    if (err) {
        return console.log(err);
    }
    parser.parse(data);
});
