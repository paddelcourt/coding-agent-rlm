import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(full_path)
    abs_working_directory = os.path.abspath(working_directory)

    try:
        if abs_file_path.startswith(abs_working_directory) is False:
            return f'Error: Cannot read "{abs_file_path}" as it is outside the permitted working directory'
            
        elif os.path.exists(abs_working_directory) is False:
            os.makedirs(abs_working_directory)
            
        
    except Exception as e:
        return f"Error: {e}"
    
    with open(abs_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{abs_file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write into file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path for executing the file.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to include in the write.",
            ),
        },
    ),
)
