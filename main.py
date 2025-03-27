from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from pydantic import BaseModel
import requests
import os

# Run using: uvicorn main:app --reload

# Initialize FastAPI app
app = FastAPI()

# Connect to MongoDB
MONGO_URL = "mongodb://localhost:27017"
client = MongoClient(MONGO_URL)
db = client.web_services
collection = db.web_project

# Define Pydantic models
class Product(BaseModel):
    ProductID: int
    Name: str
    UnitPrice: float
    StockQuantity: int
    Description: str

# API Endpoints

@app.get("/getSingleProduct")
def get_single_product(product_id: int):
    product = collection.find_one({"ProductID": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/getAll")
def get_all():
    products = list(collection.find({}, {"_id": 0}))
    return products

# use postman for testing

@app.post("/addNew")
def add_new_product(product: Product):
    if collection.find_one({"ProductID": product.ProductID}):
        raise HTTPException(status_code=400, detail="Product already exists")
    collection.insert_one(product.dict())
    return {"message": "Product added successfully"}

# use postman for testing

@app.delete("/deleteOne")
def delete_one(product_id: int):
    result = collection.delete_one({"ProductID": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@app.get("/startsWith")
def starts_with(letter: str):
    products = list(collection.find({"Name": {"$regex": f'^{letter}', "$options": "i"}}, {"_id": 0}))
    return products

@app.get("/paginate")
def paginate(start_id: int, end_id: int):
    products = list(collection.find({"ProductID": {"$gte": start_id, "$lte": end_id}}, {"_id": 0}).limit(10))
    return products

@app.get("/convert")
def convert_to_euro(product_id: int):
    product = collection.find_one({"ProductID": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Currency conversion failed")
    exchange_rate = response.json()["rates"].get("EUR", 1)
    price_in_euro = product["UnitPrice"] * exchange_rate
    return {"ProductID": product_id, "PriceInEuro": round(price_in_euro, 2)}

