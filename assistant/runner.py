from .tools import TOOLS

class CommandRunner:
    """
    Executes registered tools with given arguments.
    """
    def __init__(self, tools: dict):
        self.tools = tools

    def run(self, tool_name: str, **kwargs):
        if tool_name not in self.tools:
            return {"stdout": "", "stderr": f"Unknown tool: {tool_name}"}
        return self.tools[tool_name].call(**kwargs)
