import os
import subprocess
from assistant.model import OllamaAgent

SCRIPTS_DIR = "scripts"
agent = OllamaAgent(model_name="codellama:7b")

ACTION_WORDS = ["run", "start", "execute"]

def find_script(user_input: str):
    """
    Maps natural language to a Python script in the scripts folder.
    """
    # Normalize input
    text = user_input.lower()
    for w in ["run", "start", "execute", "script", "the", "please"]:
        text = text.replace(w, "")
    text = text.strip()

    # Normalize spaces to underscores
    normalized = text.replace(" ", "_")

    # First, try exact match in scripts folder
    for f in os.listdir(SCRIPTS_DIR):
        if normalized in f.lower():
            return os.path.join(SCRIPTS_DIR, f)

    # If not found, ask Code Llama to reason about the file
    llm_response = agent.ask(user_input)
    # Check if the response corresponds to a file
    for f in os.listdir(SCRIPTS_DIR):
        if f.lower() in llm_response.lower():
            return os.path.join(SCRIPTS_DIR, f)
    
    return None

def run_script(file_path):
    if not file_path or not os.path.exists(file_path):
        print("File not found.")
        return

    result = subprocess.run(
        ["python", file_path],
        capture_output=True,
        text=True
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")

# Main interactive loop
while True:
    user = input("You> ").strip()
    script_path = find_script(user)
    run_script(script_path)
