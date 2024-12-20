import json
import os


def save_parameters_to_file(parameters):
    try:
        with open("parameters.json", "w") as file:
            json.dump(parameters, file)
    except Exception as e:
        print(f"Error saving parameters: {e}")


def load_parameters_from_file(default_parameters):
    if os.path.exists("parameters.json"):
        try:
            with open("parameters.json", "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading parameters: {e}")
    return default_parameters