# 数字健康宠物伴侣

## 最近更新
### 2024-10-26
- 添加声音播放和聊天窗口改进
  - 增加声音效果支持
  - 添加聊天窗口高度配置
  - 添加演示模式
  - 添加音频转换工具
  - 更新窗口定位
- 添加音频和日志文件的 git 忽略配置
- 更新进程监控功能：
  - 添加内存使用跟踪（MB显示）
  - 修复监控间隔配置
  - 添加详细调试日志
  - 更新 config.json 格式
  - 修复进程监控初始化消息

## TODO
1. 为宠物添加默认对话配置
2. 研究如何使用 GLM APIs 支持对话功能
3. 研究如何使用本地 ollama APIs 支持对话功能

## 配置说明
项目使用 `config.json` 进行配置：
```json
{
    "zhipu_api_key": "你的API密钥",
    "pet": {
        "image": "happy-dog.png",
        "assets_dir": "resources/assets"
    },
    "monitor": {
        "interval": 20,
        "enabled": true,
        "demo_mode": false
    },
    "chat": {
        "window_height": 300
    }
}
```

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
     - 每T秒检查一次系统进程
     - 识别CPU/内存占用最高的进程
     - 使用LLM分析用户行为模式
     - 根据使用情况智能提醒休息和健康建议
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
│   ├─ ui/
│   │   ├── __init__.py
│   │   └── dialogs.py    # Interactive dialogs
│   └── utils/
│       ├── __init__.py
│       └── config.py     # Settings
├── resources/
│   └── assets/          # Images and animations
├── requirements.txt
└── README.md
