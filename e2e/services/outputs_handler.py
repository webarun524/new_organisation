import json
from typing import Any

from e2e.tests.operations_portal.variables import OUTPUTS_FILE


class OutputsHandler:
    @staticmethod
    def initialize_outputs_file():
        # check for file existence
        if OUTPUTS_FILE.exists():
            print(f"{OUTPUTS_FILE} already exists. Initialization skipped.")
            return
        # create empty outputs file
        OUTPUTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUTS_FILE, "w") as f:
            json.dump({}, f, indent=2)
        print(f"{OUTPUTS_FILE} has been initialized")

    @staticmethod
    def save_outputs(keyname: str, data: Any) -> dict:
        # Load existing data, or start with an empty dict
        if OUTPUTS_FILE.exists():
            with open(OUTPUTS_FILE, "r") as f:
                try:
                    existing_data = json.load(f)
                    # If the file is a list, wrap it into a dict
                    if isinstance(existing_data, list):
                        existing_data = {keyname: existing_data}
                    elif not isinstance(existing_data, dict):
                        existing_data = {}
                except json.JSONDecodeError:
                    existing_data = {}
        else:
            existing_data = {}

        # Replace the keyname field with new data
        if not isinstance(existing_data, dict):
            existing_data = {}
        existing_data[keyname] = data

        # Ensure folder exists
        OUTPUTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUTS_FILE, "w") as f:
            json.dump(existing_data, f, indent=2)

        return existing_data

    @staticmethod
    def get_outputs(keyname: str) -> Any:
        if not OUTPUTS_FILE.exists():
            raise FileNotFoundError(f"Outputs file '{OUTPUTS_FILE}' not found.")

        with open(OUTPUTS_FILE, "r") as f:
            existing_data = json.load(f)
            if keyname not in existing_data:
                raise KeyError(f"Key '{keyname}' not found in outputs file.")
            return existing_data.get(keyname, {})
