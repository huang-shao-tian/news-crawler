from newspaper import Article, Config
from datetime import datetime
from ..models.news import NewsArticle
import motor.motor_asyncio

async def crawl_article(url: str, db) -> NewsArticle:
    # 設置 newspaper 配置
    config = Config()
    config.browser_user_agent = 'Mozilla/5.0'
    config.request_timeout = 10
    
    article = Article(url, config=config)
    article.download()
    article.parse()
    article.nlp()  # 關鍵字提取
    
    news = NewsArticle(
        title=article.title,
        url=url,
        content=article.text,
        source=url.split('/')[2],
        published_date=article.publish_date,
        authors=article.authors,
        keywords=article.keywords
    )
    
    # 存入數據庫
    await db.articles.insert_one(news.dict())
    return news