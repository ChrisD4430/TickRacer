import sys
sys.path.insert(0, 'src')
from src.TempLexer import TempLexer
from src.Parser import Parser
from src.ParserOut import ParseOut

def main():
    if len(sys.argv) != 3 or sys.argv[1] not in("parse" , "lex"):
        print("Usage: tick parse <file> or tick lex <file>")
        sys.exit(1)

    filepath = sys.argv[2]
    try:
        with open(filepath, 'r') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: file not found: {filepath}")
        sys.exit(1)

    try:
        tokens = TempLexer(source).tokenize()

        if sys.argv[1] == "lex":
            for tok in tokens:
                print(tok)
        elif sys.argv[1] == "parse":
            ast    = Parser(tokens).parse()
            ParseOut(ast)

    except SyntaxError as e:
        print(f"Parse error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
