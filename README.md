```markdown
# 🦉 AI 技术简报生成器
> 基于 GLM-4 大模型的自动化技术情报系统。自动抓取、分析、生成结构化简报。
---
## ✨ 功能特性
- **多源聚合**：支持 OSChina、掘金、博客园、InfoQ、CSDN 等十余个技术社区
- **AI 深度研判**：GLM-4 提取高价值动态，生成包含背景、代码、学习的完整卡片
- **Web 可视化**：内置终端风格 Web 界面，支持历史回溯
- **自动化调度**：每 6 小时自动更新，自动清理过期数据
---
## 🚀 快速开始
### 1. 环境准备
- Python 3.10 (推荐，高版本可能存在兼容问题)
- 智谱 GLM-4 API Key ([点击获取](https://open.bigmodel.cn/))
### 2. 安装步骤
```bash
# 克隆项目
git clone https://github.com/1193396767weixr-ui/News-Gathering-Assistant.git
cd News-Gathering-Assistant/AI_glm_news_collector
# 安装依赖
pip install -r requirements.txt
```
### 3. 配置密钥
在项目根目录创建 `.env` 文件：
```env
# 必填：智谱 API Key
GLM_API_KEY=your_glm_api_key_here
# 可选：模型名称
GLM_MODEL=glm-4-flash
```
---
## 💻 使用方式
### 方式一：Web 界面 (推荐)
```bash
# 安装 Web 服务依赖
pip install uvicorn fastapi aiofiles
# 启动服务
uvicorn news_api:app --host 0.0.0.0 --port 8000
```
浏览器访问 `http://localhost:8000` 即可查看。
### 方式二：手动生成
```bash
python glm_news_collector.py
```
生成的 JSON 报告将保存在 `data/` 目录下。
### 方式三：定时任务
```bash
# 后台运行 (Linux/Mac)
nohup python scheduler.py > scheduler.log 2>&1 &
```
---
## 📂 核心文件解析
| 文件名 | 功能说明 |
| :--- | :--- |
| `glm_news_collector.py` | **核心引擎**：负责抓取新闻、调用 GLM 分析、生成并保存报告。 |
| `news_api.py` | **Web 服务**：提供 API 接口，供前端调用历史数据或触发生成。 |
| `index.html` | **前端界面**：用户交互页面，展示简报卡片及进度条。 |
| `scheduler.py` | **定时调度**：使用 apscheduler 每 6 小时自动执行一次任务。 |
| `.env` | **配置中心**：存储 API Key 等敏感信息，避免硬编码。 |
---
## ⚙️ 依赖说明
主要依赖库（详见 `requirements.txt`）：
- `fastapi` / `uvicorn`: Web 框架与服务
- `requests` / `beautifulsoup4`: 网络请求与网页解析
- `python-dotenv`: 环境变量读取
- `apscheduler`: 定时任务调度
---
## ❓ 常见问题
<details>
<summary><b>1. 运行报错：ModuleNotFoundError: No module named 'apscheduler'</b></summary>
<br>
请手动安装定时任务库：
<br>
<code>pip install apscheduler</code>
</details>
<details>
<summary><b>2. API 报错 401 或 无响应</b></summary>
<br>
请检查 <code>.env</code> 文件中的 <code>GLM_API_KEY</code> 是否正确配置，且账号余额充足。
</details>
<details>
<summary><b>3. 如何在 Windows 上后台运行定时任务？</b></summary>
<br>
建议直接运行 <code>python scheduler.py</code> 保持窗口开启，或使用计划任务配置 Python 脚本执行。
</details>
---
## 📜 许可证
[MIT License](LICENSE)
---
> 如果觉得项目有用，欢迎 Star ⭐ 支持！
```
