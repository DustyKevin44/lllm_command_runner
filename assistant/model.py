import ollama

class ReasoningAgent:
    def __init__(self, model_name: str = "codellama:7b"):
        self.model_name = model_name
        self.system_prompt = None

    def set_dynamic_prompt(self, prompt: str):
        self.system_prompt = prompt

    def ask(self, user_input: str):
        if not self.system_prompt:
            raise ValueError("System prompt not set.")

        response = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        return response["message"]["content"].strip()



import os

def get_scripts_list(scripts_dir: str):
    return [f for f in os.listdir(scripts_dir) if f.endswith(".py")]

def get_tools_list(tools_dict: dict):
    return list(tools_dict.keys())
def build_system_prompt(scripts_dir: str, tools_dict: dict):
    scripts = get_scripts_list(scripts_dir)
    tools = get_tools_list(tools_dict)

    prompt = f"""
You are a Python assistant that can run tools in the environment.
Available tools: {', '.join(tools)}
Available Python scripts in the folder '{scripts_dir}': {', '.join(scripts)}

Instructions:
1. If the user requests to run a script or tool, decide which tool to use and which script or file.
2. Output the tool and argument in the format: tool_name: argument
3. If the user input does not match any known tool or script, output the list of tools available.
4. Do not output code snippets, shell commands, or anything else.
"""
    return prompt