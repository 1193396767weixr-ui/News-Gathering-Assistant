import os
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import time
import concurrent.futures
import json
from datetime import datetime

# ── 配置加载 ──────────────────────────────────────────
script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, ".env"), override=True)

GLM_API_KEY = os.getenv("GLM_API_KEY", "").strip()
GLM_MODEL   = os.getenv("GLM_MODEL", "glm-4-flash")

# 数据存储目录
DATA_DIR = os.path.join(script_dir, "data")
os.makedirs(DATA_DIR, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"

# ── 工具函数 ──────────────────────────────────────────
def _get(url, timeout=12):
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=timeout)
        r.encoding = "utf-8"
        return r
    except Exception as e:
        print(f"    ⚠️ GET 失败 {url[:60]}: {e}")
        return None

def _post(url, json_data, timeout=12):
    try:
        r = requests.post(url, json=json_data, headers={"User-Agent": UA}, timeout=timeout)
        return r
    except Exception as e:
        print(f"    ⚠️ POST 失败 {url[:60]}: {e}")
        return None

def _parse_rss(text, label, limit=20, desc_len=250):
    clues = []
    try:
        root = ET.fromstring(text)
        for item in root.findall('.//item')[:limit]:
            title = (getattr(item.find('title'), 'text', '') or '').strip()
            desc  = (getattr(item.find('description'), 'text', '') or '')
            desc_clean = BeautifulSoup(desc, "html.parser").get_text()[:desc_len].strip()
            if title:
                clues.append(f"【{label}】{title} | {desc_clean}")
    except Exception as e:
        print(f"    ⚠️ RSS 解析失败({label}): {e}")
    return clues

def _parse_atom(text, label, limit=20, desc_len=200):
    clues = []
    NS = "{http://www.w3.org/2005/Atom}"
    try:
        root = ET.fromstring(text)
        for entry in root.findall(f".//{NS}entry")[:limit]:
            title   = (getattr(entry.find(f"{NS}title"),   'text', '') or '').strip()
            summary = (getattr(entry.find(f"{NS}summary"), 'text', '') or '')
            summary_clean = BeautifulSoup(summary, "html.parser").get_text()[:desc_len].strip()
            if title:
                clues.append(f"【{label}】{title} | {summary_clean}")
    except Exception as e:
        print(f"    ⚠️ Atom 解析失败({label}): {e}")
    return clues

# ── 数据源抓取函数 ────────────────────────────────────
def fetch_oschina_rss():
    r = _get("https://www.oschina.net/news/rss")
    clues = _parse_rss(r.text, "OSChina开源", limit=25) if r else []
    print(f"  ✅ OSChina开源: {len(clues)} 条")
    return clues

def fetch_oschina_software():
    r = _get("https://www.oschina.net/project/rss")
    clues = _parse_rss(r.text, "OSChina软件", limit=20) if r else []
    print(f"  ✅ OSChina软件: {len(clues)} 条")
    return clues

def fetch_cnblogs_rss():
    r = _get("https://feed.cnblogs.com/blog/sitehome/rss")
    clues = _parse_atom(r.text, "博客园", limit=20) if r else []
    print(f"  ✅ 博客园: {len(clues)} 条")
    return clues

def fetch_juejin_recommended():
    kws = ["架构","底层","源码","并发","优化","实践","引擎","模型","API","原理",
           "微服务","数据库","部署","调优","算法","容器","k8s","分布式","缓存",
           "消息队列","中间件","rust","go","llm","向量","embedding","rag","agent",
           "cuda","gpu","性能","高并发"]
    clues = []
    r = _post("https://api.juejin.cn/recommend_api/v1/article/recommend_all_feed",
              {"client_type":2608,"cursor":"0","id_type":2,"limit":50,"sort_type":200})
    if r:
        for item in r.json().get("data", []):
            if "item_info" not in item: continue
            info = item["item_info"]["article_info"]
            title = info.get("title",""); brief = info.get("brief_content","")[:200]
            if any(kw in title.lower() for kw in kws):
                clues.append(f"【掘金推荐】{title} | {brief}")
    print(f"  ✅ 掘金推荐: {len(clues)} 条")
    return clues

def fetch_juejin_backend():
    clues = []
    r = _post("https://api.juejin.cn/recommend_api/v1/article/recommend_cate_feed",
              {"cate_id":"6809637769959178254","cursor":"0","id_type":2,"limit":30,"sort_type":200})
    if r:
        for item in r.json().get("data", []):
            if "item_info" not in item: continue
            info = item["item_info"]["article_info"]
            title = info.get("title",""); brief = info.get("brief_content","")[:200]
            if title: clues.append(f"【掘金后端】{title} | {brief}")
    print(f"  ✅ 掘金后端: {len(clues)} 条")
    return clues

def fetch_juejin_frontend():
    clues = []
    r = _post("https://api.juejin.cn/recommend_api/v1/article/recommend_cate_feed",
              {"cate_id":"6809637767543259144","cursor":"0","id_type":2,"limit":20,"sort_type":200})
    if r:
        for item in r.json().get("data", []):
            if "item_info" not in item: continue
            info = item["item_info"]["article_info"]
            title = info.get("title",""); brief = info.get("brief_content","")[:200]
            if title: clues.append(f"【掘金前端】{title} | {brief}")
    print(f"  ✅ 掘金前端: {len(clues)} 条")
    return clues

def fetch_infoq_rss():
    r = _get("https://www.infoq.cn/feed")
    clues = _parse_rss(r.text, "InfoQ", limit=20) if r else []
    print(f"  ✅ InfoQ: {len(clues)} 条")
    return clues

def fetch_segmentfault_rss():
    r = _get("https://segmentfault.com/feeds")
    clues = _parse_atom(r.text, "SegmentFault", limit=20) if r else []
    print(f"  ✅ SegmentFault: {len(clues)} 条")
    return clues

def fetch_tencent_cloud_rss():
    clues = []
    for url in ["https://cloud.tencent.com/developer/column/rss/62",
                "https://cloud.tencent.com/developer/article/rss"]:
        r = _get(url)
        if r:
            clues = _parse_rss(r.text, "腾讯云", limit=20)
            if clues: break
    print(f"  ✅ 腾讯云: {len(clues)} 条")
    return clues

def fetch_aliyun_rss():
    r = _get("https://developer.aliyun.com/article/rss/all", timeout=15)
    clues = _parse_rss(r.text, "阿里云", limit=20) if r else []
    print(f"  ✅ 阿里云: {len(clues)} 条")
    return clues

def fetch_csdn_rss():
    clues = []
    r = _get("https://www.csdn.net/rss/index.xml")
    if r:
        kws = ["架构","源码","实战","原理","优化","AI","大模型","分布式",
               "云原生","容器","算法","数据库","中间件","微服务","性能"]
        all_items = _parse_rss(r.text, "CSDN", limit=30)
        clues = [c for c in all_items if any(kw in c for kw in kws)]
    print(f"  ✅ CSDN: {len(clues)} 条")
    return clues

def fetch_sspai_rss():
    r = _get("https://sspai.com/feed")
    clues = _parse_rss(r.text, "少数派", limit=15) if r else []
    print(f"  ✅ 少数派: {len(clues)} 条")
    return clues

def fetch_ruanyifeng_rss():
    clues = []
    for url in ["https://feeds.feedburner.com/ruanyifeng",
                "https://www.ruanyifeng.com/blog/atom.xml"]:
        r = _get(url)
        if r:
            clues = _parse_atom(r.text, "阮一峰博客", limit=15)
            if not clues: clues = _parse_rss(r.text, "阮一峰博客", limit=15)
            if clues: break
    print(f"  ✅ 阮一峰博客: {len(clues)} 条")
    return clues

# ── 并发抓取所有源 ────────────────────────────────────
def fetch_all_sources() -> list:
    sources = {
        "OSChina开源":   fetch_oschina_rss,
        "OSChina软件":   fetch_oschina_software,
        "博客园":         fetch_cnblogs_rss,
        "掘金推荐":       fetch_juejin_recommended,
        "掘金后端":       fetch_juejin_backend,
        "掘金前端":       fetch_juejin_frontend,
        "InfoQ":         fetch_infoq_rss,
        "SegmentFault":  fetch_segmentfault_rss,
        "腾讯云":         fetch_tencent_cloud_rss,
        "阿里云":         fetch_aliyun_rss,
        "CSDN":          fetch_csdn_rss,
        "少数派":         fetch_sspai_rss,
        "阮一峰博客":     fetch_ruanyifeng_rss,
    }
    all_clues = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_map = {executor.submit(fn): name for name, fn in sources.items()}
        for future in concurrent.futures.as_completed(future_map):
            name = future_map[future]
            try:
                result = future.result()
                all_clues.extend(result)
            except Exception as e:
                print(f"  ❌ {name} 异常: {e}")

    seen, deduped = set(), []
    for clue in all_clues:
        key = clue[:50]
        if key not in seen:
            seen.add(key)
            deduped.append(clue)
    print(f"\n  📦 去重后共 {len(deduped)} 条线索")
    return deduped

# ── GLM 分析（分两批共30条）──────────────────────────
def glm_batch_analysis(raw_data: str, total_clues: int, batch: int, batch_start: int) -> str:
    if not GLM_API_KEY:
        return "❌ 未配置 GLM_API_KEY"
    headers = {"Authorization": f"Bearer {GLM_API_KEY}", "Content-Type": "application/json"}
    prompt = f"""
你是一位拥有20年研发经验的首席架构师（CTO）。
我为你收集了 {total_clues} 条最新计算机技术线索，请输出第 {batch} 批（共2批），
从线索库中挑选 15 条最有价值的技术动态，编号从 {batch_start} 开始到 {batch_start+14}。
两批之间不得重复同一项目或技术。

### 🚨 铁律：
1. 禁止输出任何占位符如 `(说明痛点)` `(填写版本号)`，直接输出实质内容。
2. 本批次必须输出恰好 15 条，编号 {batch_start}～{batch_start+14}。
3. 每条必须包含具体技术名词、版本号或数据指标，拒绝空话套话。
4. 若线索不足，结合你的技术知识补充同类前沿动态。

### 每条严格按照以下格式：

## 🚀 [{batch_start}/30] [项目/技术名]：[一句话核心亮点，不超过20字]

### 🔍 背景与痛点
[2-3句话说明该技术解决的历史难题和开发者痛点]

### 🛠️ 核心硬核更新 (Deep Dive)
- **底层细节**：[具体版本号、架构变化、性能提升百分比或算法优化逻辑]
- **极简示例**：
```
[一段极短的 Python/Go/JS/Shell 示例或核心配置]
```

### 💡 为什么你应该关注它？
[对业务架构的具体冲击：省多少时间/规避什么Bug/降低多少成本，给出数字]

### 📚 零基础学习卡片
- **[最硬核专有名词]**：[用生活场景一句话类比解释]
- **上手第一步**：[具体开源库名、pip/npm 安装命令或官方文档链接]

---

**今日线索库：**
{raw_data}
"""
    data = {
        "model": GLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.35,
        "max_tokens": 8192,
    }
    try:
        resp = requests.post(
            "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            json=data, headers=headers, timeout=120
        )
        res_json = resp.json()
        if resp.status_code == 200:
            return res_json["choices"][0]["message"]["content"]
        return f"❌ API 报错（批次{batch}）：{res_json}"
    except Exception as e:
        return f"❌ 批次{batch} 研判失败：{str(e)}"

def glm_comprehensive_expert_analysis(raw_data: str, total_clues: int) -> str:
    if not GLM_API_KEY:
        return "❌ 未配置 GLM_API_KEY"
    if not raw_data.strip() or total_clues < 5:
        return f"❌ 线索不足（仅 {total_clues} 条）"
    print("  🔄 第1批（1-15条）生成中...")
    batch1 = glm_batch_analysis(raw_data, total_clues, batch=1, batch_start=1)
    print("  ✅ 第1批完成")
    time.sleep(3)
    print("  🔄 第2批（16-30条）生成中...")
    batch2 = glm_batch_analysis(raw_data, total_clues, batch=2, batch_start=16)
    print("  ✅ 第2批完成")
    return batch1 + "\n\n" + batch2

# ── 持久化存储（核心新增）────────────────────────────
def save_report(report: str, total_clues: int) -> dict:
    """保存一次生成结果到 data/ 目录，返回该条记录的 meta"""
    now = datetime.now()
    # 文件名：data/2025-02-27_14-00.json
    filename = now.strftime("%Y-%m-%d_%H-%M") + ".json"
    filepath = os.path.join(DATA_DIR, filename)

    record = {
        "id": now.strftime("%Y%m%d%H%M"),
        "timestamp": now.isoformat(),
        "display_time": now.strftime("%Y-%m-%d %H:%M"),
        "date": now.strftime("%Y-%m-%d"),
        "slot": now.strftime("%H:%M"),
        "total_clues": total_clues,
        "report": report,
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  💾 已保存: {filepath}")

    # 清理7天前的旧文件
    _cleanup_old_files(days=7)
    return record

def _cleanup_old_files(days: int = 7):
    """删除超过 days 天的记录文件"""
    from datetime import timedelta
    cutoff = datetime.now() - timedelta(days=days)
    removed = 0
    for fname in os.listdir(DATA_DIR):
        if not fname.endswith(".json"): continue
        fpath = os.path.join(DATA_DIR, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                rec = json.load(f)
            rec_time = datetime.fromisoformat(rec["timestamp"])
            if rec_time < cutoff:
                os.remove(fpath)
                removed += 1
        except:
            pass
    if removed:
        print(f"  🗑️ 清理了 {removed} 条过期记录")

def load_all_records() -> list:
    """读取所有历史记录，按时间倒序排列"""
    records = []
    for fname in sorted(os.listdir(DATA_DIR), reverse=True):
        if not fname.endswith(".json"): continue
        fpath = os.path.join(DATA_DIR, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                records.append(json.load(f))
        except:
            pass
    return records

def load_latest_record() -> dict | None:
    """读取最新一条记录"""
    records = load_all_records()
    return records[0] if records else None

# ── 完整的一次生成流程（供调度器调用）────────────────
def run_full_pipeline() -> dict:
    """抓取 + 分析 + 保存，返回记录 dict"""
    print(f"\n{'='*60}")
    print(f"⏰ 定时任务触发: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    t0 = time.time()

    clues = fetch_all_sources()
    total = len(clues)
    print(f"\n✅ 共抓取 {total} 条线索，耗时 {time.time()-t0:.1f}s")

    if total < 10:
        print("❌ 线索不足，跳过本次生成")
        return {}

    report = glm_comprehensive_expert_analysis("\n\n".join(clues), total)
    record = save_report(report, total)
    print(f"✅ 本次任务完成，总耗时 {time.time()-t0:.1f}s\n")
    return record

# ── 主执行（手动运行）────────────────────────────────
if __name__ == "__main__":
    record = run_full_pipeline()
    if record:
        print(record["report"])