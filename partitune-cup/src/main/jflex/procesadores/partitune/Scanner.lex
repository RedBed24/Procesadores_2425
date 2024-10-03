package procesadores.partitune;

/*
import java_cup.runtime.Symbol;
import procesadores.partitune.sym;
*/

%%

%class Scanner
%8bit

%standalone
/*
%cup
*/

%line
%column

%%
. { System.out.print(yytext()); }

