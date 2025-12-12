import os
import subprocess
from typing import Dict, Any

class Tool:
    """Base class for all tools."""
    def call(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

class RunPython(Tool):
    """
    Tool to run Python scripts.
    Usage: TOOLS['run_python'].call(script_name='test')
    """
    def __init__(self, scripts_dir: str = "scripts"):
        self.scripts_dir = scripts_dir

    def call(self, script_name: str):
        if not script_name:
            return {"stdout": "", "stderr": "No script name provided."}

        normalized = script_name.lower().replace(" ", "_")
        script_path = None

        # Search for a matching Python file
        for f in os.listdir(self.scripts_dir):
            if normalized in f.lower() and f.endswith(".py"):
                script_path = os.path.join(self.scripts_dir, f)
                break

        if not script_path or not os.path.exists(script_path):
            return {"stdout": "", "stderr": f"File not found: {script_name}"}

        # Execute the Python script
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True
        )

        return {"stdout": result.stdout, "stderr": result.stderr}

# Dictionary to register tools
TOOLS: Dict[str, Tool] = {}
