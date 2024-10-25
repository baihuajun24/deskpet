from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QLineEdit
from PyQt6.QtCore import Qt
import random
from services.ai_service import OpenAIService, OllamaService

class ChatWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setMaximumHeight(50)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border-radius: 10px;
                padding: 5px;
                font-size: 10pt;
            }
        """)
        layout.addWidget(self.chat_display)
        
        # Input field
        self.input_field = QLineEdit()
        self.input_field.setMaximumWidth(200)
        self.input_field.setPlaceholderText("Type here...")
        self.input_field.returnPressed.connect(self.send_message)
        self.input_field.setStyleSheet("""
            QLineEdit {
                border-radius: 10px;
                padding: 5px;
                font-size: 10pt;
            }
        """)
        layout.addWidget(self.input_field)
        
        self.setLayout(layout)
        self.setWindowTitle('Chat')
        self.setFixedSize(220, 120)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 15px;
            }
        """)
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.Tool
        )
        
        self.chat_display.setText("有什么我可以帮你分析的吗？")
    
    def send_message(self):
        message = self.input_field.text().strip()
        if message:
            self.chat_display.clear()
            self.chat_display.append(f"Pet: {self.get_response(message)}")
            self.input_field.clear()
    
    def get_response(self, message):
        responses = [
            "让我思考一下这个问题。",
            "从逻辑角度来看...",
            "有趣的观点。请具体说明。",
            "这确实值得深入分析。",
            "我明白了，让我们系统地解决这个问题。"
        ]
        return random.choice(responses)