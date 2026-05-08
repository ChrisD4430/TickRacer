import sys
sys.path.insert(0, 'src')
from src.TempLexer import TempLexer

def test(name, source, expect_success=True):
    print(f"{'='*50}")
    print(f"TEST: {name}")
    print(f"SOURCE:\n{source.strip()}\n")
    try:
        tokens = TempLexer(source).tokenize()
        for tok in tokens:
            print(tok)
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
test("basic sequence",       "ping\nwait 2\nbeep")
test("LED pattern",          "flash\nwait 1\nflash")
test("signal with code",     "signal 10\nwait 2\nsignal 20")

# Invalid
test("unknown command",      "ping\njump\nbeep",        expect_success=False)
test("wait missing arg",     "wait\nbeep",              expect_success=False)
test("wait invalid arg",     "wait hi",                 expect_success=False)
test("negative wait",        "wait -5",                 expect_success=True)  # lexer passes, parser catches
test("too many args",        "wait 2 3",                expect_success=False)
test("ping with arg",  "ping 5",   expect_success=False)
test("beep with arg",  "beep 10",  expect_success=False)
test("flash with arg", "flash 6",  expect_success=False)