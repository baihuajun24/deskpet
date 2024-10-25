import sys
import os

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

def main():
    print("Starting application...")
    app = QApplication(sys.argv)
    print("Created QApplication")
    
    window = PetWindow()
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