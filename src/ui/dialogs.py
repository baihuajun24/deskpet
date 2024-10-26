from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QLineEdit
from PyQt6.QtCore import Qt
import random
import asyncio
from services.ai_service import ZhipuAIService

class ChatWindow(QDialog):
    def __init__(self, parent=None, api_key=None):
        super().__init__(parent)
        print(f"ChatWindow initialized with API key: {api_key[:8]}..." if api_key else "ChatWindow: No API key received")
        self.api_key = api_key
        # Initialize AI service if API key is provided
        if self.api_key:
            print("Creating ZhipuAIService...")
            self.ai_service = ZhipuAIService(api_key=self.api_key)
            print("ZhipuAIService created")
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Chat display area - start with smaller default size
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setMinimumHeight(50)  # Minimum height
        self.chat_display.setMaximumHeight(50)  # Start with small height
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
        self.setFixedSize(220, 100)  # Back to smaller default size
        
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
        
        # Initial greeting
        self.chat_display.setText("今天要记得多喝水哦！有什么需要我提醒的吗？")
    
    async def get_ai_response(self, message: str) -> str:
        try:
            # Create a task for the AI response
            response = await asyncio.wait_for(
                self.ai_service.get_response(message),
                timeout=5.0  # 5 seconds timeout
            )
            return response
        except (asyncio.TimeoutError, Exception) as e:
            print(f"AI Service error or timeout: {e}")
            return self.get_fallback_response()
    
    def get_fallback_response(self):
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
    
    def send_message(self):
        message = self.input_field.text().strip()
        print(f"User message received: {message}")
        
        if message:
            old_height = self.height()
            self.chat_display.clear()
            
            if self.api_key:
                print(f"API key found: {self.api_key[:8]}...")
                try:
                    print("Attempting to get event loop...")
                    loop = asyncio.get_event_loop()
                    print("Existing event loop found")
                except RuntimeError:
                    print("No existing event loop, creating new one...")
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    print("New event loop created and set")
                
                print("Requesting AI response...")
                response = loop.run_until_complete(self.get_ai_response(message))
                print(f"AI response received: {response}")
            else:
                print("No API key found, using fallback response")
                response = self.get_fallback_response()
                print(f"Fallback response selected: {response}")
            
            # Adjust window size based on response length
            if len(response) > 20:
                self.chat_display.setMaximumHeight(150)  # Allow expansion
                self.setFixedSize(220, 150)  # Attention: change this value to change the window size
            else:
                self.chat_display.setMaximumHeight(50)  # Keep small
                self.setFixedSize(220, 120)  # Default small size
            
            self.chat_display.append(f"Pet: {response}")
            self.input_field.clear()
            
            # Adjust window position
            new_height = self.height()
            if new_height != old_height:
                pet_pos = self.parent().pos()
                self.move(
                    pet_pos.x() - (self.width() - self.parent().width()),
                    pet_pos.y() - self.height() - 10
                )
            
            print("Message displayed and input cleared")

    def display_message(self, message):
        """Display a message in the chat window."""
        old_height = self.height()
        
        # Adjust window size based on message length
        if len(message) > 20:
            self.chat_display.setMaximumHeight(150)  # Allow expansion
            self.setFixedSize(220, 200)  # Attention: change this value to change the window size
        else:
            self.chat_display.setMaximumHeight(50)  # Keep small
            self.setFixedSize(220, 120)  # Default small size
        
        # Display the message
        self.chat_display.append(f"Pet: {message}")
        
        # Adjust window position if height changed
        new_height = self.height()
        if new_height != old_height:
            pet_pos = self.parent().pos()
            self.move(
                pet_pos.x() - (self.width() - self.parent().width()),
                pet_pos.y() - self.height() - 10
            )
