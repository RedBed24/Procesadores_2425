lexer grammar Scanner;

// TOKEN : pattern;

TIPO_COMPAS : '2/4' | '3/4' | '4/4' | '6/8';
SOSTENIDO : '#';
PUNTILLO : '.';
OCTAVA : '\'' | '_';
INICIO_REPETICION : '|:';
FIN_REPETICION : ':|';
SILENCIO : '-';
BECUADRO : '%';
L_CORCHETE : '{';
R_CORCHETE : '}';
L_PARENTESIS : '(';
R_PARENTESIS : ')';
IGUAL : '=';
// BEMOL : 'b' ;
PALABRA: [A-Za-z]+;

TITULO: '"' (~["\\] | '\\' .)* '"';
TITULO_ERROR: '"'[.\n\t]'*';

BEGIN_COMMENT: '/*' -> pushMode(COMMENT_MODE);
WS : [ \t\n\r]+ -> skip;


//////////
mode COMMENT_MODE;
END_COMMENT: '*/' -> popMode;
WS_C : [ \t\n\r]+ -> skip;
NADA :. -> skip;
// \n | \t | \r {}
// <<EOF>> { System.out.printf(Utility.LEXER_ERROR_MESSAGES[Utility.LEXER_COMMENT_ERROR]); yybegin(YYINITIAL); }
// . {}