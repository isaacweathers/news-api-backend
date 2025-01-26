import boto3
from fastapi import APIRouter, HTTPException
from app.models.article_model import Article
from app.services.dynamo_services import update_article
from app.services.dynamo_services import delete_article

# Initialize the DynamoDB client
dynamodb = boto3.resource("dynamodb", region_name="us-east-2")
table = dynamodb.Table("Articles4")  # Replace "Articles" with your actual table name

router = APIRouter(
    prefix="/api/articles",
    tags=["articles"]
)


# In-memory storage for testing (replace with DynamoDB later)
#fake_db = []

# Fetch all articles
@router.get("/")
def get_articles():
    try:
        # Fetch all articles from DynamoDB
        response = table.scan()
        return {"articles": response.get("Items", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching articles: {str(e)}")


@router.get("/{article_id}")
def get_article(article_id: str):
    try:
        # Query the article by its Partition Key (PK)
        response = table.get_item(Key={"PK": f"ARTICLE#{article_id}", "SK": "VERSION#1"})
        article = response.get("Item")
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return {"article": article}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching article: {str(e)}")


@router.post("/")
def create_article(article: Article):
    try:
        # Add the article to DynamoDB
        table.put_item(
            Item={
                "PK": f"ARTICLE#{article.id}",
                "SK": "VERSION#1",
                "Title": article.title,
                "Content": article.content,
                "Tags": article.tags,
                "Author": article.author,
                "PublishedAt": article.created_at.isoformat(),
            }
        )
        return {"message": "Article created successfully", "article": article}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating article: {str(e)}")


@router.delete("/{article_id}")
def delete_article(article_id: str):
    try:
        # Delete the article by Partition Key (PK) and Sort Key (SK)
        table.delete_item(Key={"PK": f"ARTICLE#{article_id}", "SK": "VERSION#1"})
        return {"message": "Article deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting article: {str(e)}")


@router.put("/{article_id}")
def update_article_endpoint(article_id: str, updates: dict):
    try:
        result = update_article(article_id, updates)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{article_id}")
def delete_article_endpoint(article_id: str):
    try:
        result = delete_article(article_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))