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

int {return new Symbol(sym.TIPO_DATO, yytext());} /// this

<YYINITIAL> {
[a-zA-Z][a-zA-Z|0-9]* {
        if (Utility.isKeyWord(yytext())){
            System.out.printf("%s %s\n", Utility.getTokenType(yytext()),yytext());
            //return new Symbol(sym
        } else {
            System.out.printf("identificador %s\n", yytext());
            return new Symbol(sym.IDENTIFICADOR, yytext());
        }
}
2\/4 | 3\/4 | 4\/4 | 6\/8 {
    Utility.Compas compas = Utility.getCompasType(yytext());
    System.out.printf("Tipo compas %s\n", yytext());
    return new Symbol(sym.TIPO_COMPAS, compas);
}
[0-9]*\/[0-9]* {System.out.println(Utility.LEXER_ERROR_MESSAGES[Utility.LEXER_COMPAS_DURATION_ERROR]);}
# { System.out.println("sostenido"); 
    return new Symbol(sym.SOSTENIDO, yytext());
}
' | _ { System.out.println("octava");
    return new Symbol(sym.OCTAVA, yytext());
 }
\. { System.out.println("puntillo"); 
    return new Symbol(sym.PUNTILLO, yytext());
}
\|: { System.out.println("inicio repetición");
     return new Symbol(sym.PRINCIPIO_REP, yytext());}
:\| { System.out.println("fin repetición"); 
    return new Symbol(sym.FINAL_REP, yytext());}
- { System.out.println("silencio"); 
    return new Symbol(sym.SILENCIO, yytext());}
\% { System.out.println("becuadro"); 
    return new Symbol(sym.BECUADRO, yytext());}
\{ { System.out.println("token {"); 
    return new Symbol(sym.LLAVE_IZQ, yytext());
}
\} { System.out.println("token }"); 
    return new Symbol(sym.LLAVE_DER, yytext());
}
\( { System.out.println("token ("); 
    return new Symbol(sym.PARENTESIS_IZQ, yytext());
}
\) { System.out.println("token )"); 
    return new Symbol(sym.PARENTESIS_DER, yytext());
}
= { System.out.println("token ="); 
    return new Symbol(sym.IGUAL, yytext());
}
\"[^\"]*\" { System.out.printf("titulo %s\n", yytext()); 
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
