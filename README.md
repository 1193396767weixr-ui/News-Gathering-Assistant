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
git clone <https://github.com/1193396767weixr-ui/News-Gathering-Assistant>
(找到你克隆这个仓库的地址)
cd AI_glm_news_collector

4. 安装依赖
pip install -r requirements.txt
5. 配置环境变量
复制 .env.example 为 .env 并配置：
# 智谱 GLM-4 API Key（必填）
GLM_API_KEY=your_glm_api_key_here(去GLM官网获取API:https://docs.bigmodel.cn/,可选择4-flash免费的)
# GLM 模型名称（默认 glm-4-flash）
GLM_MODEL=glm-4-flash
# 新闻源（可选，用逗号分隔）
NEWS_SOURCES=https://www.ithome.com/tech/,https://www.36kr.com/information/technology/(可自行添加别的新闻源)
🎯 使用方法
方式一：手动生成
直接运行核心脚本：
python glm_news_collector.py
脚本会自动：抓取所有配置的技术源，提取有效线索（约 200+ 条），调用 GLM-4 分析并生成 30 条精选动态。并保存到 data/ 目录。

方式二：Web 服务
启动 FastAPI 后端：
# 安装 uvicorn（如果未安装）
pip install uvicorn
# 启动服务
uvicorn news_api:app --host 0.0.0.0 --port 8000
访问 http://localhost:8000 即可看到 Web 界面。

若安装uvicorn失败，可选择创建虚拟环境的方法：
# 创建虚拟环境
python3 -m venv venv
# 激活
source venv/bin/activate
# 在虚拟环境内安装（不会冲突）
pip install uvicorn fastapi aiofiles requests beautifulsoup4 python-dotenv
# 启动
uvicorn news_api:app --host 0.0.0.0 --port 8000 --reload

方式三：定时任务
后台运行调度器：
# 前台运行
python scheduler.py
# 后台运行（推荐）
nohup python scheduler.py > scheduler.log 2>&1 &
调度器会：
每 6 小时自动生成一次简报，保存到 data/ 目录，自动清理 7 天前的旧记录

对代码的核心内容阐述：
核心逻辑层：glm_news_collector.py
负责数据的抓取、清洗、AI分析与存储。读取 .env 文件中的 API Key 和模型配置。
glm_comprehensive_expert_analysis 是核心函数。它将抓取到的文本线索拼接成 Prompt（提示词），发送给智谱 GLM-4 大模型。
Prompt 工程：设定了“CTO 首席架构师”的人设，要求模型输出包含“背景痛点”、“核心更新”、“代码示例”、“学习卡片”的结构化内容，并分两批生成共 30 条动态。
将生成好的简报保存为 JSON 文件存放在 data/ 目录下。
包含 _cleanup_old_files 自动清理机制，只保留最近 7 天的数据，防止磁盘占用过大。

Web 服务层：news_api.py
这是项目的“接口层”，基于 FastAPI 框架构建，为前端页面提供数据支持。

前端展示层：index.html
用于用户交互的可视化界面。
点击“立即生成”触发异步请求，并显示实时进度。
点击左侧历史记录可无缝切换查看往期简报。

调度层：scheduler.py
用于负责定时任务的执行。
定时触发：使用 apscheduler 库，设置定时器（默认每 6 小时执行一次）。
守护进程：设计为后台运行模式。启动时会立即执行一次任务，随后按设定的时间周期循环执行。
日志记录：将运行状态（开始、成功、失败）记录到 scheduler.log 文件中，方便排查问题。

配置文件：.env
存储智谱 API Key（GLM_API_KEY），避免将密钥硬编码在 Python 代码中，方便代码分享和部署。
配置模型名称和备用的新闻源 URL。

依赖清单：requirements.txt
这是“安装说明书”。
列出了项目运行所需的 Python 第三方库：
fastapi & uvicorn：用于搭建 Web 服务。
requests：用于发送 HTTP 请求抓取网页数据。
beautifulsoup4：用于解析 HTML 提取文本。
python-dotenv：用于读取 .env 配置文件。
apscheduler：用于定时任务调度（虽然原 requirements.txt 漏掉了，但根据报错需要添加）。
