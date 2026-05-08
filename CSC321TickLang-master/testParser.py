# test_parser.py
import sys
sys.path.insert(0, 'src')
from src.TempLexer import TempLexer
from src.Parser import Parser
from src.ParserOut import ParseOut

def test(name, source, expect_success=True):
    print(f"{'='*50}")
    print(f"TEST: {name}")
    print(f"SOURCE:\n{source.strip()}\n")
    try:
        tokens = TempLexer(source).tokenize()
        ast    = Parser(tokens).parse()
        ParseOut(ast)
        print()
        if expect_success:
            print(">>> PASS")
        else:
            print(">>> FAIL (expected error but got none)")
    except SyntaxError as e:
        if not expect_success:
            print(f"Error (expected): {e}")
            print(">>> PASS")
        else:
            print(f"Error (unexpected): {e}")
            print(">>> FAIL")
    print()

# Valid
test("basic sequence",        "ping\nwait 2\nbeep",                        expect_success=True)
test("LED pattern",           "flash\nwait 1\nflash\nwait 1\nflash",       expect_success=True)
test("game event timing",     "wait 3\nsignal 1\nwait 2\nsignal 2",        expect_success=True)
test("robot movement cues",   "signal 10\nwait 2\nsignal 20\nwait 1\nsignal 10", expect_success=True)

# Invalid
test("unknown command",       "ping\njump\nbeep",                          expect_success=False)
test("wait missing arg",      "wait\nbeep",                                expect_success=False)
test("wait invalid arg",      "wait hi",                                   expect_success=False)
test("negative wait",         "wait -5",                                   expect_success=False)
test("signal missing arg",    "signal\nbeep",                              expect_success=False)
test("ping with arg",         "ping 5",                                    expect_success=False)