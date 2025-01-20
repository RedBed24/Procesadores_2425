parser grammar Parser;

options {
	tokenVocab = Scanner;
}

partitura: fragmento* obra EOF;
obra: OBRA TITULO LLAVE_IZQ especificacion* bloque_notas LLAVE_DER | error_obra;
error_obra: ID? TITULO LLAVE_IZQ especificacion* bloque_notas LLAVE_DER;

especificacion: clave | compas | armadura | error_especificacion;
error_especificacion: ID IGUAL;
clave: CLAVE IGUAL NOTA_BASE;
compas: COMPAS IGUAL COMPAS_DURACION;
armadura: ARMADURA IGUAL nota_armadura+;
nota_armadura: (BEMOL | SOSTENIDO) NOTA_BASE;
fragmento: FRAGMENTO ID LLAVE_IZQ especificacion* bloque_notas LLAVE_DER | error_fragmento;
error_fragmento: ID? ID LLAVE_IZQ especificacion* bloque_notas LLAVE_DER;
bloque_notas: LLAVE_IZQ elemento+ LLAVE_DER;
elemento: repeticion | secuencia | ligadura | llamada;
repeticion: PRINCIPIO_REP? secuencia+ FINAL_REP | error_repeticion;
error_repeticion: PRINCIPIO_REP elemento+ FINAL_REP;
ligadura: LIGADURA LLAVE_IZQ secuencia+ LLAVE_DER | error_ligadura;
error_ligadura: (LIGADURA | ID?) LLAVE_IZQ elemento+ LLAVE_DER;
llamada: ID;
secuencia: DURACION PARENTESIS_IZQ (posibles_notas)+ PARENTESIS_DER;
posibles_notas: nota | SILENCIO;
modificador: BEMOL | SOSTENIDO | BECUADRO;
nota: modificador? NOTA_BASE OCTAVA? PUNTILLO? | error_nota;
error_nota: modificador? ID OCTAVA? PUNTILLO?;
