# 🛍️ ShopSphere

A modern cloud-based NoSQL e-commerce platform built with Flask and Amazon DynamoDB.

ShopSphere demonstrates how DynamoDB Single Table Design can be used to build a scalable product catalog and review system with category filtering, ratings, reviews, and CRUD operations. The application was initially developed and tested using DynamoDB Local and later migrated to Amazon DynamoDB in AWS Academy Learner Lab.

---

## 🚀 Features

### Product Management

* Create products
* View product details
* Update products
* Delete products

### Product Reviews & Ratings

* Add customer reviews
* Rate products from 1–5 stars
* Calculate average product ratings
* Display product review history

### Category Filtering

* Browse products by category
* Powered by a DynamoDB Global Secondary Index (GSI)

### Search Functionality

* Real-time product search
* Instant filtering from the homepage

### Modern User Interface

* Dark-themed responsive design
* Interactive product cards
* Category badges
* Stock status indicators
* Modal popup for product creation
* Product detail pages
* Responsive layout for different screen sizes

---

## ☁️ Cloud Architecture

```text
User
  ↓
Web Browser
  ↓
Flask Application
  ↓
Amazon DynamoDB
     ├─ Products
     └─ Reviews

Global Secondary Index:
CategoryIndex
```

---

## 🛠 Technologies Used

### Backend

* Python
* Flask
* Boto3

### Database

* Amazon DynamoDB
* DynamoDB Single Table Design
* Global Secondary Index (GSI)

### Frontend

* HTML5
* CSS3
* JavaScript
* Jinja2 Templates

### Development Tools

* AWS Academy Learner Lab
* DynamoDB Local (Development Phase)
* Docker
* Visual Studio Code

---

## 📂 Project Structure

```text
ShopSphere/
│
├── app.py
├── db.py
├── requirements.txt
├── .env
├── README.md
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── product.html
│   └── edit_product.html
│
└── static/
```

---

## 🗄 Database Design

### Single Table Design

Table Name:

```text
ShopSphere
```

The application stores products and reviews within a single DynamoDB table.

### Product Item

```json
{
  "PK": "PRODUCT#123",
  "SK": "META",
  "product_id": "123",
  "type": "product",
  "name": "Gaming Mouse",
  "category": "Electronics",
  "price": "49.99",
  "stock": 15
}
```

### Review Item

```json
{
  "PK": "PRODUCT#123",
  "SK": "REVIEW#2026-06-06T12:30:00",
  "type": "review",
  "customer_name": "John",
  "rating": 5,
  "comment": "Excellent product!"
}
```

---

## 🔑 Primary Key Structure

### Partition Key (PK)

```text
PRODUCT#<product_id>
```

### Sort Key (SK)

Product Metadata:

```text
META
```

Reviews:

```text
REVIEW#<timestamp>
```

This design allows products and their reviews to be grouped together under the same partition key.

---

## 📌 Global Secondary Index (GSI)

### CategoryIndex

Partition Key:

category

Sort Key:

product_id

Purpose:

- Query products by category
- Support category filtering
- Avoid full table scans
- Improve application performance

---

## 📊 Query Performance & Cost Considerations

Amazon DynamoDB charges based on the number of read and write operations performed.

### Scan Operation

A Scan reads every item in a table and then applies filtering. While this approach is simple, it becomes inefficient and expensive as the dataset grows because DynamoDB must examine all items regardless of how many match the filter criteria.

Example:

Find all products in category "Electronics"

Using a Scan would require DynamoDB to read every product in the table.

### Query Operation with GSI

ShopSphere uses a Global Secondary Index (CategoryIndex) to support category filtering.

Instead of scanning the entire table, DynamoDB can directly query products that belong to a specific category.

Benefits:

- Lower read costs
- Faster response times
- Better scalability
- Reduced resource consumption

### Why CategoryIndex Was Created

The application frequently needs to retrieve products by category. Creating the CategoryIndex GSI allows these requests to use Query operations instead of Scan operations, improving both performance and cost efficiency.

### Read and Write Capacity Considerations

Every product creation, update, review submission, and deletion generates write operations.

Every product listing, product detail view, category filter, and review retrieval generates read operations.

By using:

- Single Table Design
- Efficient Partition Keys
- Global Secondary Indexes

the application minimizes unnecessary reads and supports efficient scaling as the dataset grows.

---


## 🔄 CRUD Operations

### Create

Create new products and reviews.

### Read

Retrieve products, product details, and reviews.

### Update

Modify existing product information.

### Delete

Remove products from the catalog.

---

## ⭐ Rating System

Users can submit ratings and reviews for products.

Average rating is calculated using:

```python
total = sum(review["rating"] for review in reviews)
average = total / len(reviews)
```

Ratings are displayed on product detail pages.

---

## ▶️ Running the Project

### Activate Virtual Environment

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

```env
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_SESSION_TOKEN=...
AWS_REGION=us-east-1
TABLE_NAME=ShopSphere
```

### Run Flask Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 🎯 Learning Outcomes

This project demonstrates:

* NoSQL data modeling
* Amazon DynamoDB
* Single Table Design
* Partition Keys and Sort Keys
* Global Secondary Indexes (GSI)
* CRUD operations
* Flask web development
* DynamoDB integration using Boto3
* Cloud database deployment
* Responsive UI development
* AWS Academy cloud services

---

## ☁️ Deployment Journey

### Phase 1 – Local Development

* DynamoDB Local
* Docker
* Flask
* Local testing

### Phase 2 – Cloud Migration

* AWS Academy Learner Lab
* Amazon DynamoDB
* Cloud-hosted database
* Production-style testing

---
## 📸 Application Screenshots

### Homepage
ShopSphere\Screen shots\s1.png

### Product Details Page
(Add screenshot here)

### Category Filtering
(Add screenshot here)

### Review System
(Add screenshot here)

---

## 👩‍💻 Author

**Randa Ali**

Cloud Computing Student

2026
