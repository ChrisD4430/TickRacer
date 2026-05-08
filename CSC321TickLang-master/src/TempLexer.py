from src.Token import Token
from typing import List

class TempLexer:
    def __init__(self, source: str):
        self.source = source

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        lines = self.source.splitlines()

        for line_num, line in enumerate(lines, start=1):
            line = line.split('#')[0]   # remove everything after '#' in order to propely parse code comments
            stripped = line.strip()
            if not stripped:
                continue  # skip empty lines

            parts = stripped.split()   # split on whitespace

            if not parts:
                continue

            cmd = parts[0].lower()     # make it case-insensitive for safety

            # Recognize keywords
            if cmd == "wait":
                tokens.append(Token("WAIT", "wait", line_num, 1))
            elif cmd == "ping":
                tokens.append(Token("PING", "ping", line_num, 1))
            elif cmd == "beep":
                tokens.append(Token("BEEP", "beep", line_num, 1))
            elif cmd == "flash":
                tokens.append(Token("FLASH", "flash", line_num, 1))
            elif cmd == "signal":
                tokens.append(Token("SIGNAL", "signal", line_num, 1))
            else:
                raise SyntaxError(f"Unknown command '{parts[0]}' on line {line_num}")

            if cmd in ("wait", "signal"):
                if len(parts) < 2:
                    raise SyntaxError(f"Missing argument for '{cmd}' on line {line_num}")

            if cmd in ("ping", "beep", "flash"):
                if len(parts) > 1:
                    raise SyntaxError(f"'{cmd}' takes no arguments on line {line_num}")

            # Handle argument if present
            if len(parts) > 1:
                arg = parts[1]
                if arg.lstrip('-').isdigit():
                    column = line.find(arg) + 1
                    tokens.append(Token("INTEGER", arg, line_num, column))
                else:
                    raise SyntaxError(f"Expected integer after '{parts[0]}', got '{arg}' on line {line_num}")

            if len(parts) > 2:
                raise SyntaxError(f"Too many arguments on line {line_num}")

        # Add EOF token at the end
        tokens.append(Token("EOF", "EOF", len(lines) + 1, 1))
        return tokens
