from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class NewsArticle(BaseModel):
    title: str
    url: str
    content: str
    source: str
    published_date: Optional[datetime]
    authors: List[str] = []
    keywords: List[str] = []