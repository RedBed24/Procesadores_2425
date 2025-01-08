lexer grammar Scanner;

@header {
    from ..python.utils.logger import logger
}

options {
	caseInsensitive = true;
}

COMPAS_DURACION: '2/4' | '3/4' | '4/4' | '6/8';
COMPAS_DURATION_ERROR: [0-9]+ '/' [0-9]+ {logger.error("Duracion de compas no valida", self.line, self.column);
};
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
ID: [a-z]+; 
TITULO: '"' (~["])* '"';
TITULO_ERROR: '"' [.\n\r\t]* {logger.error("Titulo no cerrado", self.line, self.column);
} -> skip;
COMMENT: '/*' .*? '*/' -> skip;
BAD_COMMENT: '/*' .*? {logger.error("Comentario sin cerrar", self.line, self.column);
} -> skip;
WS: [ \t\n\r]+ -> skip;

