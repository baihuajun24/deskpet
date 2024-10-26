import psutil
import time
from threading import Thread
from services.ai_service import ZhipuAIService
from PyQt6.QtCore import QObject, pyqtSignal
import asyncio

class ProcessMonitor(QObject):
    message_signal = pyqtSignal(str)
    
    def __init__(self, interval=10, api_key=None):
        super().__init__()
        self.interval = interval  # Seconds between process checks
        self.running = False
        self.ai_service = ZhipuAIService(api_key=api_key) if api_key else None
        print(f"ProcessMonitor initialized with interval: {self.interval} seconds")  # Updated message
        
    def get_top_process(self):
        try:
            # Get all processes and their info with elevated privileges
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'memory_percent']):
                try:
                    # Get detailed memory info
                    with proc.oneshot():  # Improve performance by getting all info at once
                        info = {
                            'pid': proc.pid,
                            'name': proc.name(),
                            'memory_percent': proc.memory_percent(),
                            'memory_mb': proc.memory_info().rss / (1024 * 1024)  # Convert to MB
                        }
                        if info['memory_percent'] > 0:
                            processes.append(info)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            # Filter and sort by memory usage
            valid_processes = [p for p in processes if p['memory_percent'] is not None]
            if not valid_processes:
                return None
                
            # Sort by memory usage and get top process
            valid_processes.sort(key=lambda x: x['memory_mb'], reverse=True)
            top_process = valid_processes[0]
            
            print(f"Top 3 processes by memory:")
            for proc in valid_processes[:3]:
                print(f"- {proc['name']}: {proc['memory_mb']:.1f}MB ({proc['memory_percent']:.1f}%)")
            
            return top_process
            
        except Exception as e:
            print(f"Error getting top process: {e}")
            return None
    
    def analyze_user_behavior(self, process_info):
        if not self.ai_service:
            return "该休息一下了，记得多喝水哦！"
        
        try:
            prompt = f"""
            用户正在使用 {process_info['name']} 程序，
            内存使用率: {process_info['memory_percent']:.1f}%。
            请分析用户可能在做什么，并给出关于休息、喝水或运动的温馨提醒。
            请用简短友好的语气回复，不超过30个字。
            """
            
            # Create event loop for this thread if it doesn't exist
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Run the async call synchronously
            response = loop.run_until_complete(self.ai_service.get_response(prompt))
            print(f"AI Response: {response}")
            return response
            
        except Exception as e:
            print(f"Error in analyze_user_behavior: {e}")
            return "工作辛苦了，别忘了适当休息哦！"
    
    def start_monitoring(self):
        """Start the monitoring process in a separate thread."""
        print("Starting process monitor...")
        self.running = True
        Thread(target=self._monitor_loop, daemon=True).start()
    
    def stop_monitoring(self):
        """Stop the monitoring process."""
        print("Stopping process monitor...")
        self.running = False
    
    def _monitor_loop(self):
        """Main monitoring loop that runs in a separate thread."""
        print("Monitor loop started")
        while self.running:
            try:
                # Get the top process
                process = self.get_top_process()
                if process:
                    # Analyze and emit message
                    message = self.analyze_user_behavior(process)
                    if message:
                        # Emit the message to be displayed in the chat window
                        self.message_signal.emit(message)
                        print(f"Monitor message sent: {message}")
                
                # Wait for next check
                time.sleep(self.interval)
                
            except Exception as e:
                print(f"Error in monitor loop: {e}")
                time.sleep(self.interval)  # Still wait before next attempt
        
        print("Monitor loop ended")
