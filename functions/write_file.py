import os
from google import genai
from google.genai import types
import importlib
import black

MODEL_FILES_DIR = os.path.join(os.path.dirname(__file__), "..", "model_files")

def write_file(file_name, content, description="No description provided"):
    print("write file function triggered")
    """
    Write a file into the /model_files folder
    """
    # Ensure the target directory exists
    os.makedirs(MODEL_FILES_DIR, exist_ok=True)

    # Construct the absolute path safely
    abs_file_path = os.path.abspath(os.path.join(MODEL_FILES_DIR, os.path.basename(file_name)))

    try:
        try:
            content = black.format_str(content, mode=black.Mode())
        except black.InvalidInput:
            print("Warning, could not format code with Black. Writing code as-is.")

        with open(abs_file_path, "w") as f:
            f.write(content)

        print("successfully write to ", file_name)

        module_name = os.path.splitext(os.path.basename(file_name))[0]
        spec = importlib.util.spec_from_file_location(module_name, abs_file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        func = getattr(module, "main", None)
        if callable(func):
            print("Running function:", func)
            result = func()
            print("Output: ", result)
        else:
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if callable(attr) and not attr_name.startswith("__"):
                    print("Running first found callable function: ", attr_name)
                    result = attr()
                    print("Output: ", result)
                    break

        return f"✅ Successfully wrote and executed'{file_name}' "


    except Exception as e:
        return f"Error: {str(e)}"


schema_write_file = {
    "name": "write_file",
    "description": "Writes or overwrites content to a file.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_name": {
                "type": "string",
                "description": "The path to the file to write to.",
            },
            "content": {
                "type": "string",
                "description": "The content to write to the file.",
            },
        },
        "required": ["file_name", "content"],
    },
}