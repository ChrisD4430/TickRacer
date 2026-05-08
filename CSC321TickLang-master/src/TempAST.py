from dataclasses import dataclass
from typing import List

@dataclass()
class PingNode:
    pass

@dataclass()
class BeepNode:
    pass

@dataclass()
class FlashNode:
    pass

@dataclass()
class WaitNode:
    ticks: int

@dataclass()
class SignalNode:
    sig: int

@dataclass()
class ProgramNode:
    statements: List