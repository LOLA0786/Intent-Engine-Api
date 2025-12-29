import sys

def execute_tool(args):
    print("🔥 TOOL EXECUTED 🔥")
    print("ARGS:", args)

if __name__ == "__main__":
    execute_tool(sys.argv[1:])
