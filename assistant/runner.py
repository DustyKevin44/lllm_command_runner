from assistant.tools import TOOLS
import json

class CommandRunner:

    def run(self, tool_call):
        if isinstance(tool_call, str):
            tool_call = json.loads(tool_call)

        tool_name = tool_call["tool"]
        args = tool_call.get("args", {})

        # Map 'arguments' to 'code' for backward compatibility
        if "arguments" in args and "code" not in args:
            args["code"] = args.pop("arguments")

        if tool_name not in TOOLS:
            return {"error": f"Unknown tool: {tool_name}"}

        return TOOLS[tool_name].call(**args)

