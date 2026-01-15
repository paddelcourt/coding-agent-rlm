import os
from google.genai import types

MAX_CHARS = 10000  # If file exceeds this, store in env var for sub-RLM

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(full_path)
    abs_working_directory = os.path.abspath(working_directory)

    try:
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{abs_file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: File not found: "{file_path}"'

        file_size = os.path.getsize(abs_file_path)

        # Large file: store in env var for sub-RLM to access via REPL
        if file_size > MAX_CHARS:
            with open(abs_file_path, "r") as f:
                content = f.read()
            env_var = "LARGE_FILE_CONTENT"
            os.environ[env_var] = content
            return f"File too large ({file_size:,} chars). Stored in {env_var} environment variable. Use call_sub_rlm to process it - the sub-agent can access it via os.environ['{env_var}']"

        # Small file: return content directly
        with open(abs_file_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get file content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
           "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path for executing the file.",
            ),
        },
    ),
)
