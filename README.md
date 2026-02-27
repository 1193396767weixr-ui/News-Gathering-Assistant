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
Python 3.8+
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
⚙️ 高级配置
修改抓取源
编辑 glm_news_collector.py 中的 fetch_all_sources() 函数，添加或删除数据源：
# 示例：添加自定义 RSS 源
def fetch_custom_rss():
    r = _get("https://your-custom-rss.com/feed")
    clues = _parse_rss(r.text, "自定义源", limit=20) if r else []
    return clues
调整 GLM 分析参数
修改 glm_comprehensive_expert_analysis() 函数中的提示词：
prompt = f"""
你是一位拥有20年研发经验的首席架构师（CTO）。
...
"""
自定义前端样式
直接修改 index.html 中的 CSS 变量：
:root {
  --accent:#00d4ff;  /* 主色调 */
  --accent2:#39ff8f; /* 辅助色 */
  --accent3:#ff5f3d; /* 强调色 */
  --accent4:#ffb700; /* 标注色 */
}
📊 API 文档
启动 Web 服务后访问：
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
主要端点
端点	方法	描述	
/	GET	Web 界面	
/api/history	GET	获取历史简报列表	
/api/report/{id}	GET	获取指定简报详情	
/api/latest	GET	获取最新简报	
/generate-news	GET	手动触发生成	
🛠️ 技术栈
后端：FastAPI + Uvicorn
前端：原生 HTML/CSS/JavaScript
AI：智谱 GLM-4 Flash
数据收集：Requests + BeautifulSoup
调度：APScheduler
📝 日志与监控
查看实时日志
tail -f scheduler.log
日志格式
2025-02-27 14:00:00 [INFO] 🚀 定时任务开始执行...
2025-02-27 14:00:05 [INFO] ✅ OSChina开源: 25 条
2025-02-27 14:00:10 [INFO] ✅ 博客园: 18 条
...
🔧 故障排查
问题：ModuleNotFoundError: No module named 'apscheduler'
解决：安装缺失依赖
pip install apscheduler
问题：GLM API 报错 401 Unauthorized
检查：确保 .env 中的 GLM_API_KEY 正确无误
问题：生成速度慢
优化：
检查网络连接
使用付费版 GLM-4 模型（响应更快）
减少抓取源数量
🌟 功能展示
1. 技术简报卡片
每条动态包含：
🔍 背景与痛点
🛠️ 核心硬核更新（含代码示例）
💡 价值分析
📚 零基础学习卡片
2. 实时生成进度
Web 界面显示生成各阶段进度：
数据抓取进度
GLM 分析进度
生成完成提示
3. 历史记录浏览
左侧边栏显示所有历史简报，点击即可查看。
📜 许可证
MIT License
🤝 贡献指南
欢迎提交 Issue 和 Pull Request！
Fork 本仓库
创建特性分支 (git checkout -b feature/AmazingFeature)
提交更改 (git commit -m 'Add some AmazingFeature')
推送到分支 (git push origin feature/AmazingFeature)
开启 Pull Request
📧 联系方式
如有问题或建议，请提交 GitHub Issue。
⭐ 如果这个项目对你有帮助，请给一个 Star！
