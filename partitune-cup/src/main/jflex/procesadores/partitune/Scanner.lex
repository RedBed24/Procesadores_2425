package procesadores.partitune;

/*
import java_cup.runtime.Symbol;
import procesadores.partitune.sym;
*/

%%

%class Scanner
%8bit

%caseless

%state COMMENT

%standalone
/*
%cup
*/

%line
%column

%%
<YYINITIAL> {
fragmento { System.out.print("token fragmento"); }
obra { System.out.print("token obra"); }
clave { System.out.print("token clave"); }
compas { System.out.print("token compas"); }
armadura { System.out.print("token armadura"); }
lig { System.out.print("token ligadura"); }
DO | RE | MI | FA | SOL | LA | SI { System.out.printf("nota %s", yytext()); }
sf | f | sc | c | n | bl | r { System.out.printf("duracion %s", yytext()); }
2\/4 | 3\/4 | 4\/4 | 6\/8 { System.out.print("duracion compas"); }
b | # { System.out.print("modificador"); }
' | _ { System.out.print("octava"); }
\. { System.out.print("puntillo"); }
\|: { System.out.print("inicio repetición"); }
:\| { System.out.print("fin repetición"); }
- { System.out.print("silencio"); }
\% { System.out.print("becuadro"); }
\{ { System.out.print("token {"); }
\} { System.out.print("token }"); }
\( { System.out.print("token ("); }
\) { System.out.print("token )"); }
= { System.out.print("token ="); }
\"[^\"]*\" { System.out.printf("titulo %s", yytext()); }
[a-zA-Z][a-zA-Z|0-9|_]* { System.out.printf("id: %s", yytext()); }
\/\* { yybegin(COMMENT); }
\n | \t | \r {}
. {}
}

<COMMENT> {
\*\/ { yybegin(YYINITIAL); }
\n | \t | \r {}
. {}
}
