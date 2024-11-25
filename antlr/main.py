from antlr4 import *
from Scanner import Scanner

def main():
    # Input arithmetic expression

    # Create input stream
    input_stream = FileStream("test.txt")

    # Create the lexer
    lexer = Scanner(input_stream)

# Itera sobre los tokens uno a uno
    print("Procesando tokens:")
    while True:
        token = lexer.nextToken()
        if token.type == Token.EOF:
            break
        print(f"Token: {token.text}, Tipo: {token.type}, Nombre {lexer.symbolicNames[token.type]}")


if __name__ == "__main__":
    main()