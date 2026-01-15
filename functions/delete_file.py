import os
from google.genai import types

def delete_file(working_directory, file_path):
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
    
    try:
        os.remove(abs_file_path)
        return f'Successfully deleted "{abs_file_path}"'
    except Exception as e:
        return f"Error deleting file: {e}"

schema_delete_file = types.FunctionDeclaration(
    name="delete_file",
    description="delete into file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path for deleting the file.",
            ),
        },
    ),
)
