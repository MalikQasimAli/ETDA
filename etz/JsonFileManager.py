import json
import os

class JsonFileManager:
        def __init__(self):
                # Hardcoded path to the default data included in the library
                package_dir = os.path.dirname(os.path.abspath(__file__))
                self.json_file_path = os.path.join(package_dir, 'data', 'etz_json.json')

        def load_data(self):
                with open(self.json_file_path, 'r') as file:
                        data = json.load(file)
                return data

        def save_data(self, data):
                with open(self.json_file_path, 'w') as file:
                        json.dump(data, file, indent=2)
