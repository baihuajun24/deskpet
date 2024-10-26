from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QLineEdit
from PyQt6.QtCore import Qt
import random
import asyncio
import os
from services.ai_service import ZhipuAIService

class ChatWindow(QDialog):
    def __init__(self, parent=None, api_key=None, window_height=300):
        super().__init__(parent)
        print(f"ChatWindow initialized with API key: {api_key[:8]}..." if api_key else "ChatWindow: No API key received")
        self.api_key = api_key
        self.dialogue_history = []  # Add this line to store dialogue history
        
        # Initialize AI service if API key is provided
        if self.api_key:
            print("Creating ZhipuAIService...")
            self.ai_service = ZhipuAIService(api_key=self.api_key)
            print("ZhipuAIService created")
        
        # Set window size
        self.setFixedWidth(300)  # Fixed width
        self.setFixedHeight(window_height)  # Configurable height
        
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
        self.chat_display.setText("嗷呜！今天又元气满满的一天呢！")
    
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
        if not message:
            return
            
        # Add user message to history
        self.dialogue_history.append({
            "role": "user",
            "content": message
        })
        
        if self.api_key:
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Get AI response with history
            response = loop.run_until_complete(
                self.get_ai_response(message, self.dialogue_history)
            )
        else:
            response = self.get_fallback_response()
        
        # Add AI response to history
        self.dialogue_history.append({
            "role": "assistant",
            "content": response
        })
        
        # Update display
        self.chat_display.setText(response)
        self.input_field.clear()

    def display_message(self, message):
        """Display a message and add to history."""
        old_height = self.height()
        
        # Add to dialogue history
        self.dialogue_history.append({
            "role": "assistant",
            "content": message
        })
        
        # Adjust window size and display message
        if len(message) > 20:
            self.chat_display.setMaximumHeight(200)
            self.setFixedSize(220, 150)
        else:
            self.chat_display.setMaximumHeight(50)
            self.setFixedSize(220, 120)
        
        self.chat_display.setText(message)
        
        # Adjust window position
        new_height = self.height()
        if new_height != old_height:
            pet_pos = self.parent().pos()
            self.move(
                pet_pos.x() - (self.width() - self.parent().width()),
                pet_pos.y() - self.height() - 10
            )

    def save_dialogue(self):
        """Save dialogue history to a log file."""
        if not self.dialogue_history:  # If no dialogue, don't save
            print("No dialogue to save")
            return
            
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create absolute path for logs directory
        log_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),  # Go up to src directory
            'logs'
        )
        print(f"Attempting to save logs to: {log_dir}")
        
        # Create directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            print(f"Created logs directory at: {log_dir}")
        
        # Create absolute path for log file
        filename = os.path.join(log_dir, f"chat_log_{timestamp}.txt")
        
        try:
            # Save the dialogue
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Chat log created at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                for entry in self.dialogue_history:
                    f.write(f"{entry['role']}: {entry['content']}\n")
            print(f"Successfully saved dialogue to: {filename}")
        except Exception as e:
            print(f"Error saving dialogue: {e}")

    def close(self):
        """Override close to save dialogue history."""
        self.save_dialogue()
        super().close()
