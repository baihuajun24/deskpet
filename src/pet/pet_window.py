from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os, sys
from ui.dialogs import ChatWindow
from monitors.process_monitor import ProcessMonitor

class PetWindow(QMainWindow):
    def __init__(self, api_key: str = None):
        print("Initializing PetWindow...")
        super().__init__()
        self.chat_window = None
        self.api_key = api_key
        
        # Initialize process monitor
        self.process_monitor = ProcessMonitor(interval=10, api_key=self.api_key)
        # Connect monitor messages to handler
        self.process_monitor.message_signal.connect(self.handle_monitor_message)
        # Start monitoring
        self.process_monitor.start_monitoring()
        
        self.initUI()
        print("PetWindow initialization complete")
    
    def handle_monitor_message(self, message):
        # If chat window doesn't exist, create it
        if not self.chat_window or not self.chat_window.isVisible():
            self.open_chat_window()
        # Display the message
        self.chat_window.display_message(message)
    
    def close_application(self):
        print("Closing application...")
        # Stop the monitor before closing
        if hasattr(self, 'process_monitor'):
            self.process_monitor.stop_monitoring()
        self.close()
        sys.exit()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Check if click is within the pet label bounds
            if self.pet_label.geometry().contains(event.pos()):
                self.open_chat_window()
            self.old_pos = event.globalPosition().toPoint()
    
    def open_chat_window(self):
        # Check if chat window already exists and is visible
        if self.chat_window is not None and self.chat_window.isVisible():
            self.chat_window.activateWindow()
            return
            
        # Create new chat window if none exists, passing the API key
        print(f"pet_window.py opening chat with API key: {self.api_key[:8]}..." if self.api_key else "No API key")
        self.chat_window = ChatWindow(self, api_key=self.api_key)  # Pass API key here
        # Position the chat window above the pet
        pet_pos = self.pos()
        self.chat_window.move(
            pet_pos.x() - (self.chat_window.width() - self.width()),  # Align right edges
            pet_pos.y() - self.chat_window.height() - 10  # Above pet with 10px gap
        )
        self.chat_window.show()
        
    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()
        
    def initUI(self):
        print("Setting up UI...")
        # Set window properties
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Load the image
        image_path = os.path.join("..", "resources", "assets", "1026.png")
        print(f"Attempting to load image from: {image_path}")
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print("Failed to load image!")
        else:
            print(f"Loaded image, size: {pixmap.width()}x{pixmap.height()}")
        
        # Create a central widget
        central_widget = QWidget()
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)
        
        # Add close button
        self.close_button = QPushButton("×", central_widget)
        self.close_button.setGeometry(80, 0, 20, 20)  # Adjusted position for smaller window
        self.close_button.clicked.connect(self.close_application)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                border-radius: 10px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        
        # Create and setup pet label
        self.pet_label = QLabel(central_widget)
        self.pet_label.setPixmap(pixmap)
        self.pet_label.setStyleSheet("background: transparent;")
        
        # Set size based on image or default to 100x100
        if not pixmap.isNull():
            # Scale down the image if it's too large
            if pixmap.width() > 200 or pixmap.height() > 200:
                scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
                self.pet_label.setPixmap(scaled_pixmap)
                width = scaled_pixmap.width()
                height = scaled_pixmap.height()
            else:
                width = pixmap.width()
                height = pixmap.height()
            
            self.pet_label.setGeometry(0, 20, width, height)
            self.setFixedSize(max(100, width), 
                            max(100, height + 20))  # +20 for close button space
        else:
            self.pet_label.setGeometry(0, 20, 100, 100)
            self.setFixedSize(100, 120)  # 100x100 plus space for close button
        
        # Replace the current self.move(100, 100) with:
        screen = self.screen()  # Get the screen where the window is
        screen_geometry = screen.availableGeometry()  # This accounts for taskbar space
        
        # Calculate position (subtract window width and height from screen dimensions)
        x = screen_geometry.width() - self.width() - 20  # 20px padding from right
        y = screen_geometry.height() - self.height() - 20  # 20px padding from bottom
        
        self.move(x, y)
        self.old_pos = self.pos()
        print("UI setup complete")
