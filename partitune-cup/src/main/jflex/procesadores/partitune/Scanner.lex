package procesadores.partitune;

/*
import java_cup.runtime.Symbol;
import procesadores.partitune.sym;
*/
import procesadores.partitune.Utility;

import java.lang.Character;

%%

%class Scanner
%8bit

%caseless

%state COMMENT

/*%standalone*/
%int
/*
%cup
*/

%line
%column

%%
<YYINITIAL> {
[a-zA-Z][a-zA-Z|0-9]* {
    if (Character.toLowerCase(yytext().charAt(0)) == 'b') {
        if (yytext().length() == 1) {
            System.out.printf("bemol\n");
        } else {
            try {
                boolean test = Utility.getTokenType(yytext().substring(1)) == Utility.TokenType.NOTA;
                System.out.printf("bemol\nNota %s\n", yytext().substring(1));
            } catch (IllegalArgumentException e) {
                System.out.printf("identificador %s\n", yytext().substring(1));
            }
        }
    }
    else {
        if (Utility.isKeyWord(yytext())){
            System.out.printf("%s %s\n", Utility.getTokenType(yytext()),yytext());
        } else {
            System.out.printf("identificador %s\n", yytext());
        }
    }
}
2\/4 | 3\/4 | 4\/4 | 6\/8 {
    Utility.Compas compas = Utility.getCompasType(yytext());
    System.out.printf("Tipo compas %s\n", yytext());
}
[0-9]*\/[0-9]* {System.out.println(Utility.LEXER_ERROR_MESSAGES[Utility.LEXER_COMPAS_DURATION_ERROR]);}
# { System.out.println("sostenido"); }
' | _ { System.out.println("octava"); }
\. { System.out.println("puntillo"); }
\|: { System.out.println("inicio repetición"); }
:\| { System.out.println("fin repetición"); }
- { System.out.println("silencio"); }
\% { System.out.println("becuadro"); }
\{ { System.out.println("token {"); }
\} { System.out.println("token }"); }
\( { System.out.println("token ("); }
\) { System.out.println("token )"); }
= { System.out.println("token ="); }
\"[^\"]*\" { System.out.printf("titulo %s\n", yytext()); }
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
