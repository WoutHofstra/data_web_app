import os


def get_functions():

    directory = "../model_files"

    try:
        return [
            f for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))
        ]
    except Exception as e:
        print(f"Error reading this directory: {directory}:", e)
        return []