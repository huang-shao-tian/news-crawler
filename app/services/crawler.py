from newspaper import Article, Config
from datetime import datetime
from ..models.news import NewsArticle
import motor.motor_asyncio
import nltk
import os

# NLTK データパスを設定
nltk.data.path.append(os.path.expanduser('~/nltk_data'))

async def crawl_article(url: str, db) -> NewsArticle:
    try:
        # newspaper の設定
        config = Config()
        config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        config.request_timeout = 20
        config.language = 'zh'
        config.fetch_images = False
        
        # デバッグログ追加
        print(f"Starting to download article from: {url}")
        
        article = Article(url, config=config)
        article.download()
        print("Article downloaded successfully")
        
        article.parse()
        print("Article parsed successfully")
        
        article.nlp()
        print("NLP processing completed")
        
        news = NewsArticle(
            title=article.title,
            url=url,
            content=article.text,
            source=url.split('/')[2],
            published_date=article.publish_date,
            authors=article.authors,
            keywords=article.keywords
        )
        
        # データベースに保存
        await db.articles.insert_one(news.dict())
        print("Article saved to database")
        
        return news
        
    except Exception as e:
        print(f"Error in crawl_article: {str(e)}")
        raise