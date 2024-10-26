from PyQt6.QtCore import QObject, pyqtSignal, QThread, Qt
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QUrl
import psutil
import asyncio
import time
import os
from services.ai_service import ZhipuAIService

class ProcessMonitor(QObject):
    message_signal = pyqtSignal(str)
    play_sound_signal = pyqtSignal()
    
    def __init__(self, interval=10, api_key=None, demo_mode=False):
        super().__init__()
        self.interval = interval
        self.running = False
        self.ai_service = ZhipuAIService(api_key=api_key) if api_key else None
        self.demo_mode = demo_mode
        
        # Initialize sound effect
        print("Initializing sound effect...")
        self.sound = QSoundEffect()
        self.sound.setLoopCount(1)
        
        # Only move to main thread if application exists
        app = QApplication.instance()
        if app:
            print("Moving sound to main thread...")
            self.sound.moveToThread(app.thread())
        else:
            print("Warning: No QApplication instance found")
        
        # Set audio file path
        audio_path = os.path.abspath(os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            '..',
            'resources',
            'assets',
            '1026.wav'
        ))
        
        print(f"Loading audio from: {audio_path}")
        
        if os.path.exists(audio_path):
            print("Audio file found!")
            url = QUrl.fromLocalFile(audio_path)
            self.sound.setSource(url)
            self.sound.setVolume(0.5)
            
            # Connect signals using queued connection
            self.play_sound_signal.connect(
                self.play_sound,
                Qt.ConnectionType.QueuedConnection
            )
            
            if self.sound.isLoaded():
                print("Sound loaded successfully!")
            else:
                print("Waiting for sound to load...")
                self.sound.loadedChanged.connect(self.on_sound_loaded)
        else:
            print(f"Audio file not found at: {audio_path}")
    
    def on_sound_loaded(self):
        """Callback for when sound loading status changes"""
        if self.sound.isLoaded():
            print("Sound loaded successfully!")
        else:
            print("Sound failed to load!")
    
    def play_sound(self):
        """Helper method to play sound (called in main thread)"""
        if not self.sound.isLoaded():
            print("Sound not loaded, cannot play!")
            return
            
        print("Playing notification sound...")
        self.sound.play()
    
    def get_top_process(self):
        try:
            # Get all processes and their info with elevated privileges
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'memory_percent']):
                try:
                    # Get detailed memory info and multiply by 10 for testing
                    with proc.oneshot():
                        memory_mb = proc.memory_info().rss / (1024 * 1024)  # Convert to MB
                        memory_percent = proc.memory_percent()
                        
                        # Multiply by 10 for testing heavy workloads
                        info = {
                            'pid': proc.pid,
                            'name': proc.name(),
                            'memory_percent': memory_percent * 10,  # 10x for testing
                            'memory_mb': memory_mb * 10  # 10x for testing
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
            
            print(f"Top 3 processes by memory (10x for testing):")
            for proc in valid_processes[:3]:
                print(f"- {proc['name']}: {proc['memory_mb']:.1f}MB ({proc['memory_percent']:.1f}%)")
            
            return top_process
            
        except Exception as e:
            print(f"Error getting top process: {e}")
            return None
    
    def analyze_user_behavior(self, process_info):
        if self.demo_mode:  # Check if demo mode is on
            message = "嘿！！朋友，别一直盯着屏幕里的代码了，我准备好去探险了！你呢？让我们站起来，去发现新世界吧！"
            self.message_signal.emit(message)
            self.play_sound_signal.emit()
            return message
        
        elif not self.ai_service:
            message = "该休息一下了，记得多喝水哦！"
            self.message_signal.emit(message)
            self.play_sound_signal.emit()  # Emit signal instead of direct play
            return message
        
        try:
            prompt = f"""
            用户正在使用 {process_info['name']} 程序，
            内存使用率: {process_info['memory_percent']:.1f}%。
            请分析用户可能在做什么，并给出关于休息、喝水或运动的温馨提醒。
            请用简短友好的语气回复，不超过30个字。
            """
            
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            response = loop.run_until_complete(self.ai_service.get_response(prompt))
            print(f"AI Response: {response}")
            message = response.strip('"')
            self.message_signal.emit(message)
            # self.play_sound_signal.emit()  # Emit signal instead of direct play
            return message
            
        except Exception as e:
            print(f"Error in analyze_user_behavior: {e}")
            message = "工作辛苦了，别忘了适当休息哦！"
            self.message_signal.emit(message)
            self.play_sound_signal.emit()  # Emit signal instead of direct play
            return message
    
    def monitor_loop(self):
        print("Monitor loop started")
        while self.running:
            process_info = self.get_top_process()
            if process_info:
                self.analyze_user_behavior(process_info)
            time.sleep(self.interval)
    
    def start_monitoring(self):
        print("Starting process monitor...")
        self.running = True
        self.monitor_thread = QThread()
        self.moveToThread(self.monitor_thread)
        self.monitor_thread.started.connect(self.monitor_loop)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        print("Stopping process monitor...")
        self.running = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.quit()
            self.monitor_thread.wait()