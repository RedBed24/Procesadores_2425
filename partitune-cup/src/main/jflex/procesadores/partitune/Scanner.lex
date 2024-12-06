package procesadores.partitune;


import java_cup.runtime.Symbol;
import procesadores.partitune.sym;
import procesadores.partitune.Utility;

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

%%


<YYINITIAL> {
[a-zA-Z][a-zA-Z|0-9]* {
        if (Utility.isKeyWord(yytext())){
            return new Symbol(Utility.getTokenType(yytext()), yytext());
        } else {
            return new Symbol(sym.ID, yytext());
        }
}
2\/4 | 3\/4 | 4\/4 | 6\/8 {
    Utility.Compas compas = Utility.getCompasType(yytext());
    return new Symbol(sym.COMPAS_DURACION, compas);
}
[0-9]*\/[0-9]* {System.out.println(Utility.LEXER_ERROR_MESSAGES[Utility.LEXER_COMPAS_DURATION_ERROR]);}
# { return new Symbol(sym.SOSTENIDO, yytext());
}
' | _ { return new Symbol(sym.OCTAVA, yytext());
 }
\. { 
    return new Symbol(sym.PUNTILLO, yytext());
}
\|: {
     return new Symbol(sym.PRINCIPIO_REP, yytext());}
:\| { 
    return new Symbol(sym.FINAL_REP, yytext());}
- { 
    return new Symbol(sym.SILENCIO, yytext());}
\% {  
    return new Symbol(sym.BECUADRO, yytext());}
\{ { 
    return new Symbol(sym.LLAVE_IZQ, yytext());
}
\} {
    return new Symbol(sym.LLAVE_DER, yytext());
}
\( { 
    return new Symbol(sym.PARENTESIS_IZQ, yytext());
}
\) { 
    return new Symbol(sym.PARENTESIS_DER, yytext());
}
= { 
    return new Symbol(sym.IGUAL, yytext());
}
\"[^\"]*\" {  
    return new Symbol(sym.TITULO, yytext());
}
\"[.|\n|\t]* { System.out.println(Utility.LEXER_ERROR_MESSAGES[Utility.LEXER_UNFINISHED_TITLE]); } // error título
\/\* { yybegin(COMMENT); }
" " | \n | \t | \r {}
. { System.out.println(Utility.LEXER_ERROR_MESSAGES[Utility.LEXER_UNKNOWN_ERROR]); }
}

<COMMENT> {
\*\/ { yybegin(YYINITIAL); }
\n | \t | \r {}
<<EOF>> { System.out.printf(Utility.LEXER_ERROR_MESSAGES[Utility.LEXER_COMMENT_ERROR]); yybegin(YYINITIAL); }
. {}
}
