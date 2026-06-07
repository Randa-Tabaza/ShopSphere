import boto3
import os
from dotenv import load_dotenv
from uuid import uuid4
from datetime import datetime
from boto3.dynamodb.conditions import Key

load_dotenv()

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN")
)

TABLE_NAME = os.getenv("TABLE_NAME")


def create_table():
    existing_tables = dynamodb.meta.client.list_tables()["TableNames"]

    if TABLE_NAME in existing_tables:
        print(f"Table '{TABLE_NAME}' already exists.")
        return

    table = dynamodb.create_table(
        TableName=TABLE_NAME,

        KeySchema=[
            {"AttributeName": "PK", "KeyType": "HASH"},
            {"AttributeName": "SK", "KeyType": "RANGE"}
        ],

        AttributeDefinitions=[
            {"AttributeName": "PK", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"},
            {"AttributeName": "category", "AttributeType": "S"},
            {"AttributeName": "product_id", "AttributeType": "S"}
        ],

        GlobalSecondaryIndexes=[
            {
                "IndexName": "CategoryIndex",
                "KeySchema": [
                    {"AttributeName": "category", "KeyType": "HASH"},
                    {"AttributeName": "product_id", "KeyType": "RANGE"}
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                }
            }
        ],

        BillingMode="PAY_PER_REQUEST"
    )

    table.wait_until_exists()
    print(f"Table '{TABLE_NAME}' created successfully!")


# =========================
# PRODUCT FUNCTIONS
# =========================

def add_product(name, description, category, price, stock, image_url):

    table = dynamodb.Table(TABLE_NAME)

    product_id = str(uuid4())

    item = {
        "PK": f"PRODUCT#{product_id}",
        "SK": "META",
        "product_id": product_id,
        "type": "product",
        "name": name,
        "description": description,
        "category": category,
        "price": str(price),
        "stock": int(stock),
        "image_url": image_url
    }

    table.put_item(Item=item)

    return product_id


def get_all_products():

    table = dynamodb.Table(TABLE_NAME)

    response = table.scan(
        FilterExpression="#t = :product",
        ExpressionAttributeNames={
            "#t": "type"
        },
        ExpressionAttributeValues={
            ":product": "product"
        }
    )

    return response["Items"]


def get_product(product_id):

    table = dynamodb.Table(TABLE_NAME)

    response = table.get_item(
        Key={
            "PK": f"PRODUCT#{product_id}",
            "SK": "META"
        }
    )

    return response.get("Item")


def update_product(
    product_id,
    name,
    description,
    category,
    price,
    stock,
    image_url
):

    table = dynamodb.Table(TABLE_NAME)

    table.update_item(
        Key={
            "PK": f"PRODUCT#{product_id}",
            "SK": "META"
        },
        UpdateExpression="""
        SET #n = :name,
            description = :description,
            category = :category,
            price = :price,
            stock = :stock,
            image_url = :image_url
        """,
        ExpressionAttributeNames={
            "#n": "name"
        },
        ExpressionAttributeValues={
            ":name": name,
            ":description": description,
            ":category": category,
            ":price": str(price),
            ":stock": int(stock),
            ":image_url": image_url
        }
    )


def delete_product(product_id):

    table = dynamodb.Table(TABLE_NAME)

    table.delete_item(
        Key={
            "PK": f"PRODUCT#{product_id}",
            "SK": "META"
        }
    )


# =========================
# REVIEW FUNCTIONS
# =========================

def add_review(product_id, customer_name, rating, comment):

    table = dynamodb.Table(TABLE_NAME)

    timestamp = datetime.now().isoformat()

    review = {
        "PK": f"PRODUCT#{product_id}",
        "SK": f"REVIEW#{timestamp}",
        "type": "review",
        "customer_name": customer_name,
        "rating": int(rating),
        "comment": comment,
        "timestamp": timestamp
    }

    table.put_item(Item=review)


def get_reviews(product_id):

    table = dynamodb.Table(TABLE_NAME)

    response = table.query(
        KeyConditionExpression=
        Key("PK").eq(f"PRODUCT#{product_id}") &
        Key("SK").begins_with("REVIEW#")
    )

    reviews = response["Items"]

    reviews.sort(
        key=lambda x: x["timestamp"],
        reverse=True
    )

    return reviews


def get_average_rating(product_id):

    reviews = get_reviews(product_id)

    if not reviews:
        return 0

    total = sum(review["rating"] for review in reviews)

    return round(total / len(reviews), 1)

def get_products_by_category(category):

    table = dynamodb.Table(TABLE_NAME)

    response = table.query(
        IndexName="CategoryIndex",
        KeyConditionExpression=
        Key("category").eq(category)
    )

    return response["Items"]

def get_categories():

    products = get_all_products()

    categories = sorted(
        list(
            set(
                product["category"]
                for product in products
            )
        )
    )

    return categories