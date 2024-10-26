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
        
        # Change this line:
        self.chat_display.setText("今天要记得多喝水哦！")
    
    def send_message(self):
        message = self.input_field.text().strip()
        if message:
            self.chat_display.clear()
            self.chat_display.append(f"Pet: {self.get_response(message)}")
            self.input_field.clear()
    
    def get_response(self, message):
        responses = [
            "该喝水啦！保持水分很重要哦～",
            "要不要起来走动走动？久坐对身体不好呢。",
            "提醒您该休息一下眼睛了，看看远处吧！",
            "工作这么久了，起来活动活动筋骨吧！",
            "记得保持良好的坐姿哦，别驼背～",
            "该补充水分了，一起来喝杯水吧！",
            "建议您起来伸个懒腰，活动一下～",
            "要不要去倒杯温水？记得照顾好自己！"
        ]
        return random.choice(responses)