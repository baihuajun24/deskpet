import sys
import os
import json

# Debug current directory
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

try:
    print("Attempting to import QApplication...")
    from PyQt6.QtWidgets import QApplication
    print("Successfully imported QApplication")
    
    print("Attempting to import PetWindow...")
    from pet.pet_window import PetWindow
    print("Successfully imported PetWindow")
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def load_config():
    try:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        with open(config_path, 'r') as f:
            return json.load(f)
        print("config.json loaded")
    except FileNotFoundError:
        print("Error: config.json not found. Please create one from config.template.json")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: config.json is not valid JSON")
        sys.exit(1)

def main():
    print("Starting application...")
    config = load_config()
    app = QApplication(sys.argv)
    print("Created QApplication")
    
    window = PetWindow(api_key=config.get('zhipu_api_key'))
    print(f"1026 check API key: {config.get('zhipu_api_key')}")
    print("Created PetWindow")
    
    window.show()
    print("Showed window")
    
    print("Entering main event loop...")
    sys.exit(app.exec())

if __name__ == "__main__":
    print("Script is being run directly")
    main()
else:
    print("Script is being imported")
