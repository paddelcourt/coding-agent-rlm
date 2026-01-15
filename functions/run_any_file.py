import os
import subprocess
from google.genai import types
import sys

def run_any_file(working_directory, file_path, args=None, runner=None):
    full_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(full_path)
    abs_working_directory = os.path.abspath(working_directory)

    args = args or []

    if abs_file_path.startswith(abs_working_directory) is False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
    elif os.path.exists(abs_file_path) is False:
        return f'Error: File "{file_path}" not found.'
    
    
    try:
        
        if runner:
            if isinstance(runner, str):
                return "runner must be a list/tuple of tokens, not a string"
            elif not isinstance(runner, (list, tuple)):
                return "runner must be a list/tuple of tokens"
            base = list(runner)

        elif abs_file_path.endswith('.py') is True:
            base = [sys.executable]

        elif os.access(abs_file_path, os.X_OK):
            base = []

        else:
            return "Not executable and no runner provided."
    

        cmd = [*base, abs_file_path, *args]
        result = subprocess.run(cmd, timeout=30, cwd=abs_working_directory, capture_output=True)        


        if result.returncode != 0:
            return f"STDOUT: {result.stdout.decode('utf-8')}, STDERR: {result.stderr.decode('utf-8')} Process exited with code {result.returncode}"
        elif not result.stdout and not result.stderr:
            return "No output produced"
        else:
            return f"STDOUT: {result.stdout}, STDERR: {result.stderr}"

        

    except Exception as e:
        return f"Error: executing file: {e}"
    

schema_run_any_file = types.FunctionDeclaration(
    name="run_any_file",
    description="Run any file in the directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path for executing the file.",
            ),
            "runner": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Runner tokens, e.g. ['bash'] or ['node']",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="args to pass through the run python command for exectuing files.",
            ),


            
        },
    ),
)

    
    