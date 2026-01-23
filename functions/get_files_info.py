import os
from google.genai import types

def get_files_info(working_directory, file_path="."):
         full_path = os.path.join(working_directory, file_path)
         abs_path = os.path.abspath(full_path)
         abs_working_dir = os.path.abspath(working_directory)
         
         try:
            if abs_path.startswith(abs_working_dir) is False:
                return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
            elif os.path.isdir(abs_path) is False:
                return f'Error: "{file_path}" is not a directory'
            else:
                files_directory = os.listdir(abs_path)
                lines = []
                for i in files_directory:
                    file_path = os.path.join(abs_path, i)
                    size = os.path.getsize(file_path)
                    is_dir = os.path.isdir(file_path)
                    lines.append(f"- {i}: file_size={size} bytes, is_dir={(is_dir)}")
                return "\n".join(lines)
         except Exception as e:
            return f"Error: {e}"
            

            
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
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
