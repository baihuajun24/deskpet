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
            config = json.load(f)
        print("config.json loaded")  # Move print before return
        print(f"Loaded monitor interval: {config.get('monitor', {}).get('interval')} seconds")  # Add this line
        return config
    except FileNotFoundError:
        print("Error: config.json not found. Please create one from config.template.json")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: config.json is not valid JSON")
        sys.exit(1)

def main():
    print("Starting application...")
    config = load_config()
    print(f"Loaded config: {config}")
    app = QApplication(sys.argv)
    print("Created QApplication")
    
    window = PetWindow(
        api_key=config.get('zhipu_api_key'),
        pet_config=config.get('pet'),
        monitor_config=config.get('monitor'),
        chat_config=config.get('chat')
    )
    print(f"Pet config: {config.get('pet')}")
    print(f"Monitor config: {config.get('monitor')}")
    print(f"Chat config: {config.get('chat')}")
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
