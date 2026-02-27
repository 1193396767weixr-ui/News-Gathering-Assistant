from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import os
from glm_news_collector import (
    fetch_all_sources,
    glm_comprehensive_expert_analysis,
    save_report,
    load_all_records,
    load_latest_record,
    run_full_pipeline,
)

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/api/history")
def get_history():
    """返回所有历史简报的列表（不含正文，只含 meta）"""
    records = load_all_records()
    return {
        "status": "success",
        "total": len(records),
        "records": [
            {
                "id": r["id"],
                "display_time": r["display_time"],
                "date": r["date"],
                "slot": r["slot"],
                "total_clues": r["total_clues"],
            }
            for r in records
        ]
    }

@app.get("/api/report/{report_id}")
def get_report(report_id: str):
    """按 ID 返回某条简报的完整内容"""
    records = load_all_records()
    for r in records:
        if r["id"] == report_id:
            return {"status": "success", "record": r}
    return {"status": "error", "msg": "记录不存在"}

@app.get("/api/latest")
def get_latest():
    """返回最新一条简报"""
    record = load_latest_record()
    if record:
        return {"status": "success", "record": record}
    return {"status": "empty", "msg": "暂无数据，请先生成"}

@app.get("/generate-news")
def generate_news():
    """手动触发生成（兼容旧接口）"""
    record = run_full_pipeline()
    if not record:
        return {"status": "error", "msg": "生成失败，线索不足"}
    return {
        "status": "success",
        "total_clues": record["total_clues"],
        "report": record["report"],
        "display_time": record["display_time"],
        "id": record["id"],
    }