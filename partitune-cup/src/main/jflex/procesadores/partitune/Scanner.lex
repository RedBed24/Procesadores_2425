package procesadores.partitune;


import java_cup.runtime.Symbol;
import procesadores.partitune.sym;
import procesadores.partitune.partitune.*;
import procesadores.partitune.utils.*;

import java.lang.Character;

%%

%class Scanner
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
            return symbol(KeyWords.getTokenType(yytext()), yytext());
        } else {
            return symbol(sym.ID, yytext());
        }
}
2\/4 | 3\/4 | 4\/4 | 6\/8 {
    return symbol(sym.COMPAS_DURACION, yytext());
}
[0-9]*\/[0-9]* {System.out.printf(Errors.LEXER_ERROR_MESSAGES[Errors.LEXER_COMPAS_DURATION_ERROR], yyline, yycolumn);}
# { return symbol(sym.SOSTENIDO, yytext()); }
' | _ { return symbol(sym.OCTAVA, yytext());}
\. { 
    return symbol(sym.PUNTILLO, yytext());
}
\|: {
     return symbol(sym.PRINCIPIO_REP, yytext());}
:\| { 
    return symbol(sym.FINAL_REP, yytext());}
- { 
    return symbol(sym.SILENCIO, yytext());}
\% {  
    return symbol(sym.BECUADRO, yytext());}
\{ { 
    return symbol(sym.LLAVE_IZQ, yytext());
}
\} {
    return symbol(sym.LLAVE_DER, yytext());
}
\( { 
    return symbol(sym.PARENTESIS_IZQ, yytext());
}
\) { 
    return symbol(sym.PARENTESIS_DER, yytext());
}
= { 
    return symbol(sym.IGUAL, yytext());
}
\"[^\"]*\" {  
    return symbol(sym.TITULO, yytext());
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
