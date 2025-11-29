import os
import importlib
import black
import base64

MODEL_FILES_DIR = os.path.join(os.path.dirname(__file__), "..", "model_files")

def write_file(content):
    """
    Saves Python code from params['content'] to a file and executes it.
    Expects params dict with keys:
        - file_name: str
        - content: str
    """
    print("write_file function triggered")
    file_name = "main.py"

    nice_content = strip_backticks(content)

    os.makedirs(MODEL_FILES_DIR, exist_ok=True)
    abs_file_path = os.path.abspath(os.path.join(MODEL_FILES_DIR, os.path.basename(file_name)))

    try:
        try:
            nice_content = black.format_str(nice_content, mode=black.Mode())
            print("Formatted code successfully")
        except black.InvalidInput:
            print("Warning: Could not format code with Black. Writing as-is.")

        with open(abs_file_path, "w") as f:
            f.write(nice_content)
        print(f"File saved: {abs_file_path}")

        if abs_file_path.endswith(".py"):
            module_name = os.path.splitext(os.path.basename(file_name))[0]
            spec = importlib.util.spec_from_file_location(module_name, abs_file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            func = getattr(module, "main", None)
            if callable(func):
                print("Running main() function")
                result = func()
                return result if result is not None else "main() returned None"

            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if callable(attr) and attr_name.startswith("create"):
                    print(f"Running function: {attr_name}")
                    result = attr()
                    return result if result is not None else f"{attr_name} returned None"

            return "Error: No callable functions found in module"

        else:
            return f"File saved: {abs_file_path} (not a Python file, execution skipped)"

    except Exception as e:
        return f"Error: {str(e)}"
    

def strip_backticks(code: str):

    new_lines = []
    lines = code.splitlines()

    for line in lines:
        if not line.startswith("```"):
            new_lines.append(line)

    return "\n".join(new_lines)