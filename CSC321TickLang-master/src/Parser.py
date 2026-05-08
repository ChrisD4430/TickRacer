from src.TempAST import PingNode, BeepNode, FlashNode, WaitNode, SignalNode, ProgramNode

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos    = 0

    def current(self):
        return self.tokens[self.pos]

    def consume(self, expected_type=None):
        tok = self.current()
        if expected_type and tok.type != expected_type:
            raise SyntaxError(
                f"Line {tok.line}: Expected {expected_type} but got '{tok.value}'"
            )
        self.pos += 1
        return tok

    def match(self, *types):
        return self.current().type in types

    def parse(self):
        return self.parse_program()

    def parse_program(self):
        statements = []
        while not self.match('EOF'):
            statements.append(self.parse_statement())
        self.consume('EOF')
        return ProgramNode(statements)

    def parse_statement(self):
        tok = self.current()
        if tok.type == 'WAIT':
            return self.parse_wait()
        elif tok.type == 'PING':
            return self.parse_ping()
        elif tok.type == 'BEEP':
            return self.parse_beep()
        elif tok.type == 'SIGNAL':
            return self.parse_signal()
        elif tok.type == 'FLASH':
            return self.parse_flash()
        else:
            raise SyntaxError(f"Line {tok.line}: Unknown command '{tok.value}'")

    def parse_wait(self):
        cmd = self.consume('WAIT')
        arg = self.consume('INTEGER')
        n   = int(arg.value)
        if n < 0:
            raise SyntaxError(f"Line {cmd.line}: 'wait' event cannot be negative (got {n})")
        return WaitNode(ticks=n)

    def parse_ping(self):
        self.consume('PING')
        return PingNode()

    def parse_beep(self):
        self.consume('BEEP')
        return BeepNode()

    def parse_signal(self):
        cmd = self.consume('SIGNAL')
        arg = self.consume('INTEGER')
        n = int(arg.value)
        if n < 0:
            raise SyntaxError(f"Line {cmd.line}: 'signal' event cannot be negative (got {n})")
        return SignalNode(sig=int(arg.value))

    def parse_flash(self):
        self.consume('FLASH')
        return FlashNode()