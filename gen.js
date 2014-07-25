var ebnfParser = require('ebnf-parser');
var fs = require('fs');

fs.readFile(process.argv[2], 'utf8', function (err,data) {
    if (err) {
        return console.log(err);
    }
    grammar = ebnfParser.parse(data);
    console.log(grammar.bnf);
});
