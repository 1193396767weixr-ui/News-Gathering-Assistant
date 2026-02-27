"""
scheduler.py — 每6小时自动生成一次技术简报并保存
用法：
    source venv/bin/activate
    python scheduler.py &          # 后台运行
    nohup python scheduler.py > scheduler.log 2>&1 &  # 推荐：后台持久运行
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from glm_news_collector import run_full_pipeline
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("scheduler.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

def job():
    log.info("🚀 定时任务开始执行...")
    try:
        record = run_full_pipeline()
        if record:
            log.info(f"✅ 简报生成成功，时间: {record.get('display_time')}, 线索数: {record.get('total_clues')}")
        else:
            log.warning("⚠️ 本次任务未生成有效简报")
    except Exception as e:
        log.error(f"❌ 任务异常: {e}", exc_info=True)

if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")

    # 每6小时执行一次（00:00 / 06:00 / 12:00 / 18:00）
    scheduler.add_job(
        job,
        trigger=IntervalTrigger(hours=6),
        id="news_job",
        name="技术简报自动生成",
        replace_existing=True,
        max_instances=1,       # 防止重叠执行
        misfire_grace_time=300 # 允许5分钟内的延迟触发
    )

    log.info("⏰ 调度器启动，每6小时自动生成技术简报")
    log.info(f"🕐 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info("📌 执行时间点: 每天 00:00 / 06:00 / 12:00 / 18:00")

    # 启动时立即执行一次
    log.info("🔄 启动时立即执行一次...")
    job()

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.info("🛑 调度器已停止")