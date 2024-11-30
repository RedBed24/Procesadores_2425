lexer grammar Scanner;

options {
	caseInsensitive = true;
}

COMPAS_DURACION: '2/4' | '3/4' | '4/4' | '6/8';
SOSTENIDO: '#';
PUNTILLO: '.';
OCTAVA: '\'' | '_';
PRINCIPIO_REP: '|:';
FINAL_REP: ':|';
SILENCIO: '-';
BECUADRO: '%';
LLAVE_IZQ: '{';
LLAVE_DER: '}';
PARENTESIS_IZQ: '(';
PARENTESIS_DER: ')';
IGUAL: '=';
BEMOL: 'b';
NOTA_BASE: 'do' | 're' | 'mi' | 'fa' | 'sol' | 'la' | 'si';
DURACION: 'sf' | 'f' | 'sc' | 'c' | 'n' | 'bl' | 'r';
OBRA: 'obra';
CLAVE: 'clave';
COMPAS: 'compas';
FRAGMENTO: 'fragmento';
LIGADURA: 'lig';
ARMADURA: 'armadura';
ID: [a-z]+; // blas -> b como bemol y las palabra, debería ser: blas como palabra
// en parser, necesitamos token FRAGMENTO, aquí no aparece...
// no podemos tener un reconocedor de "palabra"

TITULO: '"' (~["\\] | '\\' .)* '"';
//TITULO_ERROR: '"'[.\n\t]'*';

BEGIN_COMMENT: '/*' -> pushMode(COMMENT_MODE), skip;
WS : [ \t\n\r]+ -> skip;


//////////
mode COMMENT_MODE;
END_COMMENT: '*/' -> popMode, skip;
NADA :. -> skip;
//FIN: EOF;
