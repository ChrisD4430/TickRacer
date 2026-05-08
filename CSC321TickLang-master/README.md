# Tick

Tick is a minimal timed-event scripting language for sequencing actions with simple, predictable timing. Programs execute strictly from top to bottom.

## Overview

A Tick program is a sequence of commands, for example:

    ping
    wait 2
    signal 5
    flash

Each command executes in order. The `wait n` command advances the internal clock by `n` ticks. There are no variables, loops, or branches, so behavior is easy to reason about.

## Repository Structure

    CSC321TickLang/
      main.py
      pyproject.toml
      uv.lock

      src/
        Parser.py
        ParserOut.py
        TempAST.py
        Token.py
        (lexer helpers)

      tests/
        valid.tick
        valid2.tick
        invalid.tick
        testLexer.py
        testParser.py

      .idea/

## Language Features

Supported commands:

- `wait n` – delay the next action by `n` ticks (non-negative integer)
- `ping` – emit a "ping" event
- `beep` – emit a "beep" event
- `signal n` – emit a numeric signal (non-negative integer)
- `flash` – emit a "flash" event

Execution model:

- Linear, top-to-bottom execution
- Only integer arguments
- No variables
- No loops
- No conditionals
- No functions

Error handling:

- Negative wait times
- Negative signal values
- Unknown commands
- Invalid or missing arguments

## Running Tick Programs

In the terminal type:

    python main.py <parse/lex> <path-to-tick-file>

Example:

    python main.py parse tests/valid1.tick

    python main.py lex tests/valid3.tick

    python main.py lex tests/invalid5.tick
