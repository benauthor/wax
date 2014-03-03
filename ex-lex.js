/*globals console: false, process: false */
var fs = require('fs'),
    Parser = require("jison").Parser,
    Lexer = require("lex"),
    html = require("html");

// load grammar from wax.json
var wax = JSON.parse(fs.readFileSync("wax.json"));

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
var spacesPerIndent = 4;
var lastIndent = 0;
// lexer.addRule(/\n/, function () {
//     console.log('nl');
// });
// lexer.addRule(/\[/, function () { return 'INDENT'; }); // ditto
// lexer.addRule(/\]/, function () { return 'DEDENT'; }); // ditto
lexer.addRule(/\s+/, function (match) {
    var indent,
        indentDiff,
        spaces = match.replace(/\n/g, ''),
        tokens = [];
    if (match[0] === "\n") {
        indent = spaces.length / spacesPerIndent;
        if (parseInt(indent, 10) !== indent) {
            throw "Bad indentation!"; // TODO line numbers
        }
        if (indent > lastIndent) {
            indentDiff = indent - lastIndent;
            tokens.push("INDENT");
            lastIndent = indent;
            return tokens;
        } else if (indent < lastIndent) {
            indentDiff = lastIndent - indent;
            for (var i = 0; i < indentDiff; i++) {
                tokens.push("DEDENT");
            }
            lastIndent = indent;
            return tokens;
        }


    }
}); // this will change for significant whitespace
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
    var parsedWax = parser.parse(data),
        pretty = html.prettyPrint(parsedWax, {indent_size: 4});
    console.log(pretty);
});
