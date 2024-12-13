from celery import Celery
from .config import settings

celery_app = Celery(
    "news_crawler",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Taipei',
    enable_utc=True,
)

@celery_app.task
def crawl_news_task(url: str):
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        import asyncio
        from .services.crawler import crawl_article
        
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.NEWS_DB]
        

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(crawl_article(url, db))
        loop.close()
        
        return {"status": "success", "article": result.dict()}
    except Exception as e:
        return {"status": "error", "message": str(e)}