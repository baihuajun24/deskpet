from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os, sys
from ui.dialogs import ChatWindow
from monitors.process_monitor import ProcessMonitor
from PyQt6.QtWidgets import QApplication

class PetWindow(QMainWindow):
    def __init__(self, api_key: str = None, pet_config: dict = None, monitor_config: dict = None, chat_config: dict = None):
        super().__init__()
        self.api_key = api_key
        self.pet_config = pet_config or {}
        self.monitor_config = monitor_config or {}
        self.chat_config = chat_config or {}  # Store chat config
        self.chat_window = None  # Initialize chat_window attribute
        
        # Initialize process monitor
        if self.monitor_config.get("enabled", True):
            self.process_monitor = ProcessMonitor(
                interval=self.monitor_config.get("interval", 10),
                api_key=self.api_key,
                demo_mode=self.monitor_config.get("demo_mode", False)  # Get demo mode from config
            )
            self.process_monitor.message_signal.connect(self.display_monitor_message)
            self.process_monitor.start_monitoring()
        
        self.initUI()
    
    def display_monitor_message(self, message):
        """Display monitor message and handle chat window"""
        print(f"Received monitor message: {message}")
        
        try:
            # Create chat window if it doesn't exist
            if not hasattr(self, 'chat_window') or self.chat_window is None:
                print("Creating new chat window...")
                self.chat_window = ChatWindow(
                    self, 
                    self.api_key,
                    window_height=self.chat_config.get("window_height", 300)  # Pass height
                )
            
            # Show message in chat window
            if not self.chat_window.isVisible():
                print("Showing chat window...")
                self.chat_window.show()
                self.position_chat_window()
            
            print("Displaying message in chat window...")
            self.chat_window.display_message(message)
            
        except Exception as e:
            print(f"Error in display_monitor_message: {e}")
            import traceback
            traceback.print_exc()
    
    def position_chat_window(self):
        """Position chat window above the pet"""
        if self.chat_window:
            chat_pos = self.pos()
            chat_pos.setY(chat_pos.y() - self.chat_window.height() - 10)
            self.chat_window.move(chat_pos)
    
    def close_application(self):
        print("Closing application...")
        # Save chat logs if chat window exists
        if self.chat_window:
            print("Saving chat logs before closing...")
            self.chat_window.save_dialogue()
        
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
        """Open chat window manually"""
        if not hasattr(self, 'chat_window') or self.chat_window is None:
            self.chat_window = ChatWindow(
                self, 
                self.api_key,
                window_height=self.chat_config.get("window_height", 300)  # Pass height
            )
        self.chat_window.show()
        self.position_chat_window()
        
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
        
        # Load the image using config
        image_path = os.path.join(
            os.path.dirname(__file__), 
            "..", 
            "..",
            self.pet_config["assets_dir"],
            self.pet_config["image"]
        )
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
        self.close_button.setGeometry(80, 0, 20, 20)
        self.close_button.clicked.connect(self.close_application)  # Make sure this is connected
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
