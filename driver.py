from assistant.model import ReasoningAgent, build_system_prompt
from assistant.runner import CommandRunner
from assistant.tools import RunPython, TOOLS

SCRIPTS_DIR = "scripts"

# Initialize tools
TOOLS["run_python"] = RunPython(scripts_dir=SCRIPTS_DIR)
runner = CommandRunner(TOOLS)

# Initialize agent
agent = ReasoningAgent(model_name="codellama:7b")

# Dynamically generate system prompt
dynamic_prompt = build_system_prompt(SCRIPTS_DIR, TOOLS)
agent.set_dynamic_prompt(dynamic_prompt)

# Interactive loop
while True:
    user_input = input("You> ").strip()
    response = agent.ask(user_input)

    # Expecting tool_name: argument format
    if ":" in response:
        tool_name, arg = map(str.strip, response.split(":", 1))
        if tool_name not in TOOLS:
            print(f"Unknown tool. Available tools: {', '.join(TOOLS.keys())}")
            continue
        result = runner.run(tool_name, script_name=arg)
    else:
        # Fallback: treat as filename for default tool
        tool_name = "run_python"
        arg = response
        result = runner.run(tool_name, script_name=arg)

    if result["stdout"]:
        print(result["stdout"], end="")
    if result["stderr"]:
        print(result["stderr"], end="")
