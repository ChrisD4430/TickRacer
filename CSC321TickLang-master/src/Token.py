from dataclasses import  dataclass

@dataclass()
class Token:
    type: str  # "IDENTIFIER", "INTEGER", "EOF"
    value: str  # e.g. "wait", "42", "ping"
    line:int = 1 # which line the token is on
    column:int =1  # which character position on that line

#test
#tok = Token(type='WAIT', value='wait', line=1)
#print(tok)
# Token(type='WAIT', value='wait', line=1)