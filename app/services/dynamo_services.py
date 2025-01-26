import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB resource
dynamodb = boto3.resource("dynamodb", region_name="us-east-2")
table = dynamodb.Table("Articles4")  # Replace "Articles" with your table name

def delete_article(article_id: str, version: str = "VERSION#1"):
    try:
        table.delete_item(
            Key={
                "PK": f"ARTICLE#{article_id}",
                "SK": version
            }
        )
        return {"message": f"Article {article_id} deleted successfully."}
    except ClientError as e:
        raise Exception(f"Error deleting article: {e.response['Error']['Message']}")

def update_article(article_id: str, updates: dict, version: str = "VERSION#1"):
    try:
        # Build the update expression dynamically
        update_expression = "SET " + ", ".join(f"{key} = :{key}" for key in updates.keys())
        expression_values = {f":{key}": value for key, value in updates.items()}

        response = table.update_item(
            Key={
                "PK": f"ARTICLE#{article_id}",
                "SK": version
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ReturnValues="UPDATED_NEW"
        )
        return {"message": f"Article {article_id} updated successfully.", "updated_attributes": response["Attributes"]}
    except ClientError as e:
        raise Exception(f"Error updating article: {e.response['Error']['Message']}")


# Create an article in DynamoDB
def create_article(article):
    try:
        table.put_item(Item=article)
        return {"message": "Article created successfully"}
    except ClientError as e:
        raise Exception(f"Error: {e.response['Error']['Message']}")

# Fetch all articles
def get_all_articles():
    try:
        response = table.scan()
        return response["Items"]
    except ClientError as e:
        raise Exception(f"Error: {e.response['Error']['Message']}")
