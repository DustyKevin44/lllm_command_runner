# assistant/tools.py
import subprocess
import sys
import tempfile
from pydantic import BaseModel

class Tool(BaseModel):
    name: str
    description: str

    def call(self, **kwargs):
        raise NotImplementedError


class RunPython(Tool):
    name: str = "run_python"
    description: str = "Execute Python code and return stdout/stderr"

    def call(self, code: str):
        """
        Runs Python code safely in a subprocess.
        """
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        process = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True
        )

        return {
            "stdout": process.stdout,
            "stderr": process.stderr,
            "returncode": process.returncode
        }


TOOLS = {
    "run_python": RunPython(),
}
import os

def find_python_file(user_input):
    """
    Map natural-language input to a file in the scripts folder.
    Example: "hello world" -> "hello_world.py" or "helloWorld.py"
    """
    scripts = [f for f in os.listdir("scripts") if f.endswith(".py")]
    # Normalize input
    normalized = user_input.lower().replace("run ", "").replace("start ", "").replace("execute ", "").replace(" ", "_")
    
    # Try to find exact match
    for f in scripts:
        fname = f.lower().replace(".py", "")
        if normalized == fname or normalized.replace("_", "") == fname.replace("_", ""):
            return os.path.join("scripts", f)
    return None


