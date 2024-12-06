lexer grammar Scanner;

options {
	caseInsensitive = true;
}

COMPAS_DURACION: '2/4' | '3/4' | '4/4' | '6/8';
COMPAS_DURATION_ERROR: [0-9]+ '/' [0-9]+ {print(f"ERROR: Duracion de compas no valida, linea {self.line}, columna {self.column}")};
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
// en parser, necesitamos token FRAGMENTO, aquí no aparece... no podemos tener un reconocedor de
// "palabra" " el personaje \"pepito\" "
TITULO: '"' (~["])* '"';
TITULO_ERROR: '"' [.\n\r\t]* {print(f"Error: Titulo no cerrado, linea {self.line}, columna {self.column}");}->skip;

COMMENT: '/*' .*? '*/' -> skip;
BAD_COMMENT: '/*' .*? {print(f"ERROR: Comentario sin cerrar, linea {self.line}, columna {self.column}")} -> skip;
WS: [ \t\n\r]+ -> skip;

