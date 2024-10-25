# 数字健康宠物伴侣

## TODO
1. default dialog for pet in xxx_config
2. figure out how to use GLM APIs to support dialogs.py
3. figure out how to use local ollama APIs to support dialogs.py


## 产品简介
针对长时间坐姿办公人群的 AI 宠物互动式健康促进应用。

## 开发任务分配
- 华君：负责软件开发（功能 1、2、4）
- 鑫祥：负责提供宠物姿态设计（功能 3）

## 核心功能
1. 基础程序
   - 后台运行的 .exe 程序
   - 无显卡依赖要求
   
2. 用户行为监测
   - 监测用户正在使用的程序进程
   - 基于时间追踪的智能提醒
   - 每30分钟提醒用户喝水

3. 宠物动态展示
   - 支持多种宠物姿态
   - 类似动态桌面的效果

4. 交互功能
   - 点击宠物弹出对话框
   - 支持对话及关闭操作

## 可选功能
5. 聊天系统
   - 支持与宠物进行对话交互

6. 姿势提醒
   - 可选择是否使用摄像头
   - 支持无摄像头模式下的提醒

## 设计特性
7. 提醒展示
   - 重要提醒时可占用整个屏幕

8. 桌面互动
   - 支持宠物趴在窗口边缘
   - 互动效果示例：
     - 喷水动画效果
     - 连续打字30分钟后会拖拽窗口
   - 参考项目：《关于我在桌面上养了只会拖来奇怪的东西和抢鼠标的鸭子这件事》
     
9. 数据统计
   - 【可选】记录程序使用时长

## Project Structure
```
DeskPet/
├── src/
│   ├── main.py           # Entry point
│   ├── pet/
│   │   ├── __init__.py
│   │   ├── pet_window.py # Main pet window
│   │   └── animations.py # Pet animations
│   ├── monitors/
│   │   ├── __init__.py
│   │   ├── process_monitor.py
│   │   └── posture_monitor.py
│   ├── services/         # New directory
│   │   ├── __init__.py
│   │   └── ai_service.py # AI service implementations
│   ├── ui/
│   │   ├── __init__.py
│   │   └── dialogs.py    # Interactive dialogs
│   └── utils/
│       ├── __init__.py
│       └── config.py     # Settings
├── resources/
│   └── assets/          # Images and animations
├── requirements.txt
└── README.md
