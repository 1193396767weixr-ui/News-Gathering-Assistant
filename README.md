🦉 AI 技术简报生成器
一个基于 GLM-4 大模型的自动化技术情报收集与生成系统。自动从多个中文技术社区抓取最新动态，生成结构化的技术简报，并提供 Web 界面查看。
✨ 功能特性
多源聚合：自动抓取 OSChina、博客园、掘金、InfoQ、SegmentFault、腾讯云、阿里云、CSDN、少数派等平台
AI 分析：使用 GLM-4 大模型深度分析技术趋势，筛选高价值动态
结构化报告：生成包含背景、核心更新、学习路径的详细技术简报
Web 可视化：精美的技术终端风格 Web 界面
历史记录：自动保存历史简报，支持回溯查看（保留 7 天）
定时任务：每 6 小时自动更新，无需人工干预
📦 项目结构
.
├── .env                  # 环境配置文件
├── glm_news_collector.py # 核心收集与分析脚本
├── news_api.py           # FastAPI Web 服务
├── index.html            # Web 前端界面
├── scheduler.py          # 定时任务调度器
├── requirements.txt      # Python 依赖
└── data/                 # 生成的简报存储目录
    └── YYYY-MM-DD_HH-MM.json
🚀 快速开始
1. 环境要求
Python 3.10（比较稳定，若使用3.10以上的版本，例如3.15是无法布置环境的）
智谱 GLM-4 API Key（从 智谱开放平台 获取）
2. 克隆项目
git clone <your-repo-url>
cd ai-news-generator
3. 安装依赖
pip install -r requirements.txt
4. 配置环境变量
复制 .env.example 为 .env 并配置：
# 智谱 GLM-4 API Key（必填）
GLM_API_KEY=your_glm_api_key_here
# GLM 模型名称（默认 glm-4-flash）
GLM_MODEL=glm-4-flash
# 新闻源（可选，用逗号分隔）
NEWS_SOURCES=https://www.ithome.com/tech/,https://www.36kr.com/information/technology/
🎯 使用方法
方式一：手动生成
直接运行核心脚本：
python glm_news_collector.py
脚本会自动：
抓取所有配置的技术源
提取有效线索（约 200+ 条）
调用 GLM-4 分析并生成 30 条精选动态
保存到 data/ 目录
方式二：Web 服务
启动 FastAPI 后端：
# 安装 uvicorn（如果未安装）
pip install uvicorn
# 启动服务
uvicorn news_api:app --host 0.0.0.0 --port 8000
访问 http://localhost:8000 即可看到 Web 界面。
Web 功能：
查看历史简报
手动触发生成
查看生成进度
切换不同日期的简报
方式三：定时任务
后台运行调度器：
# 前台运行
python scheduler.py
# 后台运行（推荐）
nohup python scheduler.py > scheduler.log 2>&1 &
调度器会：
每 6 小时自动生成一次简报
保存到 data/ 目录
自动清理 7 天前的旧记录

