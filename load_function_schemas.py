import importlib
import pkgutil
import model_files

def load_function_schemas():

    schemas = []

    from functions.call_function import call_function
    from get_functions import schema_get_functions
    from functions.write_file import schema_write_file
    from functions.getfunctions import get_functions
    schemas.extend([schema_write_file, schema_get_functions])

    for module_info in pkgutil.iter_modules(model_files.__path__):
        if not module_info.name.startswith("_"):  # Skip __init__.py and private files
            module = importlib.import_module(f"{model_files.__name__}.{module_info.name}")
            for name, value in vars(module).items():
                if name.startswith("schema_") and isinstance(value, dict):
                    schemas.append(value)
                    print(f"✅ Loaded schema: {name} from {module_info.name}.py")

    return schemas