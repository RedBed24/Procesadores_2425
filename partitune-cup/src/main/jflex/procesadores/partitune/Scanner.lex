package procesadores.partitune;


import java_cup.runtime.Symbol;
import procesadores.partitune.sym;
import procesadores.partitune.utils.*;
import procesadores.partitune.partitune.*;

import java.lang.Character;

%%

%class Scanner
%public
%8bit

%caseless

%state COMMENT

/*%standalone*/
%int

%cup
%line
%column

%{ /*-------- Custom symbol to store line and column information --------*/
    /* TODO */
    private Symbol symbol(int type){
        return new Symbol(type, yyline, yycolumn);
    }

    private Symbol symbol(int type, Object value){
        return new Symbol(type, yyline, yycolumn, value);
    }
%}

%%


<YYINITIAL> {
[a-zA-Z][a-zA-Z|0-9]* {
        if (KeyWords.isKeyWord(yytext())){
            try{
                int num_sym = KeyWords.getTokenType(yytext());
                return symbol(num_sym, KeyWords.returnPartituneObject(num_sym, yytext()));
            } catch (Exception e){
                System.out.printf(Errors.LEXER_ERROR_MESSAGES[Errors.LEXER_UNKNOWN_ERROR], yyline, yycolumn);
                System.out.println(e.getMessage());
            }
        } else {
            return symbol(sym.ID, new String(yytext()));
        }
}
2\/4 | 3\/4 | 4\/4 | 6\/8 {
    return symbol(sym.COMPAS_DURACION, Compas.getCompasType(yytext()));
}
[0-9]*\/[0-9]* {System.out.printf(Errors.LEXER_ERROR_MESSAGES[Errors.LEXER_COMPAS_DURATION_ERROR], yyline, yycolumn);}
# { return symbol(sym.SOSTENIDO, Modificador.getModificadorType(sym.SOSTENIDO)); }
' | _ { return symbol(sym.OCTAVA, Octava.getOctaveType(yytext()));}
\. { 
    return symbol(sym.PUNTILLO);
}
\|: {
     return symbol(sym.PRINCIPIO_REP);}
:\| { 
    return symbol(sym.FINAL_REP);}
- { 
    return symbol(sym.SILENCIO);}
\% {  
    return symbol(sym.BECUADRO, Modificador.getModificadorType(sym.BECUADRO) );}
\{ { 
    return symbol(sym.LLAVE_IZQ);
}
\} {
    return symbol(sym.LLAVE_DER);
}
\( { 
    return symbol(sym.PARENTESIS_IZQ);
}
\) { 
    return symbol(sym.PARENTESIS_DER);
}
= { 
    return symbol(sym.IGUAL);
}
\"[^\"]*\" {  
    return symbol(sym.TITULO, new String(yytext()));
}
\"[.|\n|\t]* { System.out.printf(Errors.LEXER_ERROR_MESSAGES[Errors.LEXER_UNFINISHED_TITLE], yyline, yycolumn); } // error título
\/\* { yybegin(COMMENT); }
" " | \n | \t | \r {}
. { System.out.printf(Errors.LEXER_ERROR_MESSAGES[Errors.LEXER_UNKNOWN_ERROR]); }
}

<COMMENT> {
\*\/ { yybegin(YYINITIAL); }
\n | \t | \r {}
<<EOF>> { System.out.printf(Errors.LEXER_ERROR_MESSAGES[Errors.LEXER_COMMENT_ERROR], yyline, yycolumn); yybegin(YYINITIAL); }
. {}
}
