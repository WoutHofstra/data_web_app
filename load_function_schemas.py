import importlib
import pkgutil
from google.genai import types
import functions

def load_function_schemas():
    schemas: list[types.FunctionDeclaration] = []

    for module_info in pkgutil.iter_modules(functions.__path__):
        if module_info.name.startswith("_"):  # skip __init__.py and private modules
            continue

        module = importlib.import_module(f"{functions.__name__}.{module_info.name}")

        for name, value in vars(module).items():
            if name.startswith("schema_") and isinstance(value, dict) and value:
                try:
                    # Convert the dict into a FunctionDeclaration
                    func_decl = types.FunctionDeclaration(
                        name=value.get("name", name.replace("schema_", "")),
                        description=value.get("description", "No description provided"),
                        parameters=value.get("parameters", {}),
                    )
                    schemas.append(func_decl)
                    print(f"✅ Loaded FunctionDeclaration: {name} from {module_info.name}.py")
                except Exception as e:
                    print(f"⚠️ Failed to convert {name} to FunctionDeclaration: {e}")

    if not schemas:
        print("⚠️ No function schemas found in model_files")

    return schemas
