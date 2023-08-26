from pydantic import BaseModel
from typing import List, Optional


class Article(BaseModel):
    title: Optional[str] = ""
    snippet: Optional[str] = ""
    message: str = ""


class ListArticle(BaseModel):
    docs: List[Article]
