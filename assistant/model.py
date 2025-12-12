import ollama

class OllamaAgent:
    def __init__(self, model_name: str = "codellama:7b"):
        self.model_name = model_name

    def ask(self, prompt: str):
        """
        Sends the user input to Code Llama to reason about which script to run.
        Returns the script name or reasoning text.
        """
        sys_prompt = """
You are a Python assistant. The user may give commands like 'run test', 'start hello world', or 'please execute the script program'.
Your task:
1. Identify which Python script in the 'scripts' folder the user wants to run.
2. Return only the filename (e.g., test.py, hello_world.py, program.py) if you are confident.
3. Do not output Python code to execute. The driver will execute the file.
4. If unsure, return a short reasoning text.
"""
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response["message"]["content"].strip()
