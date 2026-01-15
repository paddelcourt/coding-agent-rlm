import os
from google.genai import types

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(full_path)
    abs_working_directory = os.path.abspath(working_directory)
    MAX_CHARS = 10000

    try:
        if abs_file_path.startswith(abs_working_directory) is False:
            return f'Error: Cannot read "{abs_file_path}" as it is outside the permitted working directory {abs_working_directory}'
            
        elif os.path.isfile(abs_file_path) is False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(abs_file_path, "r") as f:
                return f.read(MAX_CHARS)
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
