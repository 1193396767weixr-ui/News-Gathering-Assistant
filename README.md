# 🦉 AI 技术简报生成器
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![GLM-4](https://img.shields.io/badge/AI-GLM--4-green.svg)](https://open.bigmodel.cn/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
> 一个基于 GLM-4 大模型的自动化技术情报收集与生成系统。自动从多个中文技术社区抓取最新动态，生成结构化的技术简报，并提供 Web 界面查看。
---
## 📑 目录
- [✨ 功能特性](#-功能特性)
- [🚀 快速开始](#-快速开始)
  - [环境要求](#1-环境要求)
  - [克隆项目](#2-克隆项目)
  - [安装依赖](#3-安装依赖)
  - [配置环境变量](#4-配置环境变量)
- [🎯 使用方法](#-使用方法)
  - [方式一：手动生成](#方式一手动生成)
  - [方式二：Web 服务](#方式二web服务)
  - [方式三：定时任务](#方式三定时任务)
- [🔧 核心模块解析](#-核心模块解析)
- [📁 项目结构](#-项目结构)
- [📊 API 文档](#-api-文档)
- [🛠️ 故障排查](#️-故障排查)
- [🤝 贡献指南](#-贡献指南)
- [📜 许可证](#-许可证)
---
## ✨ 功能特性
| 特性 | 描述 |
|------|------|
| 🔍 **多源聚合** | 自动抓取 OSChina、博客园、掘金、InfoQ、SegmentFault、腾讯云、阿里云、CSDN、少数派等平台 |
| 🤖 **AI 分析** | 使用 GLM-4 大模型深度分析技术趋势，筛选高价值动态 |
| 📄 **结构化报告** | 生成包含背景、核心更新、学习路径的详细技术简报 |
| 🎨 **Web 可视化** | 精美的技术终端风格 Web 界面 |
| 📚 **历史记录** | 自动保存历史简报，支持回溯查看（保留 7 天） |
| ⏰ **定时任务** | 每 6 小时自动更新，无需人工干预 |
---
## 🚀 快速开始
### 1. 环境要求
- **Python 3.10**（推荐使用 3.10 版本，3.11+ 可能存在兼容性问题）
- **智谱 GLM-4 API Key**（从 [智谱开放平台](https://open.bigmodel.cn/) 获取）
### 2. 克隆项目
```bash
git clone https://github.com/1193396767weixr-ui/News-Gathering-Assistant.git
cd News-Gathering-Assistant/AI_glm_news_collector
```
### 3. 安装依赖
```bash
pip install -r requirements.txt
```
<details>
<summary>💡 提示：如果遇到依赖冲突，建议使用虚拟环境</summary>
```bash
# 创建虚拟环境
python3 -m venv venv
# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate
# 安装依赖
pip install -r requirements.txt
```
</details>
### 4. 配置环境变量
创建 `.env` 文件并配置以下内容：
```env
# 智谱 GLM-4 API Key（必填）
# 获取地址：https://open.bigmodel.cn/
# 推荐使用免费的 glm-4-flash 模型
GLM_API_KEY=your_glm_api_key_here
# GLM 模型名称（默认 glm-4-flash）
GLM_MODEL=glm-4-flash
# 新闻源（可选，用逗号分隔）
NEWS_SOURCES=https://www.ithome.com/tech/,https://www.36kr.com/information/technology/
```
---
## 🎯 使用方法
### 方式一：手动生成
直接运行核心脚本：
```bash
python glm_news_collector.py
```
**脚本执行流程：**
1. 📡 抓取所有配置的技术源
2. 🔍 提取有效线索（约 200+ 条）
3. 🤖 调用 GLM-4 分析并生成 30 条精选动态
4. 💾 保存到 `data/` 目录
---
### 方式二：Web 服务
#### 快速启动
```bash
# 安装 uvicorn（如果未安装）
pip install uvicorn
# 启动服务
uvicorn news_api:app --host 0.0.0.0 --port 8000
```
访问 **http://localhost:8000** 即可看到 Web 界面。
#### 使用虚拟环境（推荐）
```bash
# 创建虚拟环境
python3 -m venv venv
# 激活虚拟环境
source venv/bin/activate
# 安装所需依赖
pip install uvicorn fastapi aiofiles requests beautifulsoup4 python-dotenv
# 启动服务（开发模式）
uvicorn news_api:app --host 0.0.0.0 --port 8000 --reload
```
---
### 方式三：定时任务
#### 前台运行（测试用）
```bash
python scheduler.py
```
#### 后台运行（生产环境推荐）
```bash
# 后台运行
nohup python scheduler.py > scheduler.log 2>&1 &
# 查看日志
tail -f scheduler.log
```
**调度器功能：**
- ⏰ 每 6 小时自动生成一次简报
- 💾 保存到 `data/` 目录
- 🗑️ 自动清理 7 天前的旧记录
---
## 🔧 核心模块解析
### 核心逻辑层：`glm_news_collector.py`
**职责：** 数据的抓取、清洗、AI 分析与存储
```python
# 核心函数
glm_comprehensive_expert_analysis()  # AI 分析研判
```
**关键特性：**
- 📖 读取 `.env` 文件中的 API Key 和模型配置
- 🎯 **Prompt 工程**：设定"CTO 首席架构师"人设，输出结构化内容
  - 背景痛点
  - 核心更新
  - 代码示例
  - 学习卡片
- 📦 分两批生成共 30 条动态
- 🗑️ `_cleanup_old_files` 自动清理机制（保留 7 天）
---
### Web 服务层：`news_api.py`
**职责：** 基于 FastAPI 框架的接口层
**主要端点：**
| 端点 | 方法 | 描述 |
|------|------|------|
| `/` | GET | Web 界面 |
| `/api/history` | GET | 历史简报列表 |
| `/api/report/{id}` | GET | 指定简报详情 |
| `/generate-news` | GET | 手动触发生成 |
---
### 前端展示层：`index.html`
**职责：** 用户交互的可视化界面
**交互功能：**
- 🖱️ 点击"立即生成"触发异步请求，显示实时进度
- 📜 点击左侧历史记录无缝切换查看往期简报
---
### 调度层：`scheduler.py`
**职责：** 定时任务执行
**技术实现：**
- 📦 使用 `apscheduler` 库
- ⏰ 默认每 6 小时执行一次
- 🔄 启动时立即执行一次
- 📝 日志记录到 `scheduler.log`
---
### 配置文件：`.env`
**职责：** 存储敏感配置信息
```env
GLM_API_KEY=xxx        # 智谱 API Key
GLM_MODEL=glm-4-flash  # 模型名称
NEWS_SOURCES=xxx       # 新闻源 URL
```
---
### 依赖清单：`requirements.txt`
**核心依赖：**
| 库名 | 用途 |
|------|------|
| `fastapi` & `uvicorn` | Web 服务框架 |
| `requests` | HTTP 请求 |
| `beautifulsoup4` | HTML 解析 |
| `python-dotenv` | 配置文件读取 |
| `apscheduler` | 定时任务调度 |
---
## 📁 项目结构
```
AI_glm_news_collector/
├── .env                    # 环境配置
├── .env.example            # 配置模板
├── glm_news_collector.py   # 核心收集脚本
├── news_api.py             # Web 服务
├── index.html              # 前端界面
├── scheduler.py            # 定时调度器
├── requirements.txt        # 依赖清单
├── scheduler.log           # 运行日志
└── data/                   # 数据存储目录
    └── YYYY-MM-DD_HH-MM.json
```
---
## 📊 API 文档
启动 Web 服务后访问：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
---
## 🛠️ 故障排查
<details>
<summary>❌ 问题：ModuleNotFoundError: No module named 'apscheduler'</summary>
**解决方案：**
```bash
pip install apscheduler
```
</details>
<details>
<summary>❌ 问题：GLM API 报错 401 Unauthorized</summary>
**检查项：**
1. `.env` 文件中的 `GLM_API_KEY` 是否正确
2. API Key 是否有效（未过期）
3. 是否有足够的调用额度
</details>
<details>
<summary>❌ 问题：生成速度慢</summary>
**优化建议：**
1. 检查网络连接
2. 使用付费版 GLM-4 模型（响应更快）
3. 减少抓取源数量
4. 调整并发线程数
</details>
---
## 🤝 贡献指南
欢迎提交 Issue 和 Pull Request！
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request
---
## 📜 许可证
本项目采用 [MIT License](LICENSE) 开源协议。
---
## 📞 联系方式
如有问题或建议，请提交 [GitHub Issue](https://github.com/1193396767weixr-ui/News-Gathering-Assistant/issues)。
---
<div align="center">
**⭐ 如果这个项目对你有帮助，请给一个 Star！**
[⬆ 返回顶部](#-ai-技术简报生成器)
</div>
