parser grammar Parser;

options {
	tokenVocab = Scanner;
}

partitura: fragmento* obra EOF;
obra: OBRA TITULO LLAVE_IZQ especificacion* bloque_notas LLAVE_DER;

especificacion: (clave | compas | armadura);
clave: CLAVE IGUAL NOTA_BASE;
compas: COMPAS IGUAL COMPAS_DURACION;
armadura: ARMADURA IGUAL notas_armadura;
notas_armadura: ((BEMOL | SOSTENIDO) NOTA_BASE OCTAVA?)+;
fragmento: FRAGMENTO ID LLAVE_IZQ especificacion* bloque_notas LLAVE_DER;
bloque_notas: LLAVE_IZQ elemento+ LLAVE_DER;
elemento: repeticion | secuencia | ligadura | llamada;
repeticion: PRINCIPIO_REP? secuencia+ FINAL_REP;
ligadura: LIGADURA LLAVE_IZQ secuencia+ LLAVE_DER;
llamada: ID;
secuencia: DURACION PARENTESIS_IZQ (SILENCIO | nota)+ PARENTESIS_DER;
modificador: BEMOL | SOSTENIDO | BECUADRO;
nota: modificador? NOTA_BASE OCTAVA? PUNTILLO?;
