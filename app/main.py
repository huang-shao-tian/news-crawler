from fastapi import FastAPI, BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
from .celery_app import crawl_news_task
from .models.news import NewsArticle

app = FastAPI(title="News Crawler")

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.NEWS_DB]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

@app.post("/crawl/{source}")
async def crawl_news(source: str, background_tasks: BackgroundTasks):
    if source not in settings.NEWS_SOURCES:
        return {"error": "Source not supported"}
    
    url = settings.NEWS_SOURCES[source]
    task = crawl_news_task.delay(url)
    
    return {
        "message": f"Started crawling {source}",
        "task_id": task.id
    }

@app.get("/articles/", response_model=list[NewsArticle])
async def get_articles(skip: int = 0, limit: int = 10):
    articles = await app.mongodb.articles.find().skip(skip).limit(limit).to_list(limit)
    return articles

@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task = crawl_news_task.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None
    }