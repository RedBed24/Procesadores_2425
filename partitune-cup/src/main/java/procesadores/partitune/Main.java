package procesadores.partitune;

import procesadores.partitune.Scanner;

import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;

class Main {
      private static Reader AbrirLector(String args[]) 
  {
    Reader lector = null ;
   
    if ( args.length > 0 ) 
    {
       try
       {
          lector = new FileReader(args[0]) ;
       }
       catch( IOException exc )
       {
          System.err.println("imposible abrir archivo '"+args[0]+"'");
          System.err.println("causa: "+exc.getMessage()) ;
          System.exit(1) ;
       }
 
       System.out.println("leyendo archivo '"+args[0]+"'");
    }
    else 
    {
       lector = new InputStreamReader(System.in) ;  
       System.out.println("leyendo entrada estándard (terminar con ctrl-d)");
    }
    
    return lector ;
  }

  /***************************************************************************/

  public static void main(String args[]) throws IOException 
  {
      Scanner analizador = new Scanner(AbrirLector(args)) ;
      analizador.yylex();
  }   
}
