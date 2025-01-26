from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Article(BaseModel):
    id: str                     # Unique ID for the article
    title: str                  # Article title
    content: str                # Main article content
    tags: Optional[List[str]]   # Optional list of tags
    author: str                 # Author name
    created_at: datetime = datetime.now()  # Timestamp
