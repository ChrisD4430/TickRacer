from src.TempAST import PingNode, BeepNode, FlashNode, WaitNode, SignalNode, ProgramNode

def ParseOut(node, indent=0):
    pad = "  " * indent
    if isinstance(node, ProgramNode):
        print(f"{pad}Program")
        for stmt in node.statements:
            ParseOut(stmt, indent + 1)
    elif isinstance(node, WaitNode):
        print(f"{pad}Wait({node.ticks})")
    elif isinstance(node, SignalNode):
        print(f"{pad}Signal({node.sig})")
    elif isinstance(node, PingNode):
        print(f"{pad}Ping")
    elif isinstance(node, BeepNode):
        print(f"{pad}Beep")
    elif isinstance(node, FlashNode):
        print(f"{pad}Flash")
    else:
        print(f"{pad}Unknown({node})")