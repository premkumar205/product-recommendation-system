from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from model import recommend_products

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset
df = pd.read_excel("data.xlsx")
df.fillna('', inplace=True)

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "E-commerce Recommendation API Running"}

# ---------------- ALL PRODUCTS ----------------
@app.get("/products")
def get_products():
    return df.head(50).to_dict(orient="records")

# ---------------- SINGLE PRODUCT ----------------
@app.get("/product/{product_id}")
def get_product(product_id: int):
    product = df[df['Product_ID'] == product_id]
    if product.empty:
        return {"error": "Product not found"}
    return product.to_dict(orient="records")[0]

# ---------------- SEARCH ----------------
@app.get("/search")
def search_products(query: str):
    results = df[df['Product_Name'].str.contains(query, case=False)]
    return results.head(20).to_dict(orient="records")

# ---------------- CATEGORY ----------------
@app.get("/category/{category_name}")
def get_by_category(category_name: str):
    results = df[df['Category'].str.contains(category_name, case=False)]
    return results.head(20).to_dict(orient="records")

# ---------------- TOP RATED ----------------
@app.get("/top-rated")
def top_rated():
    results = df.sort_values(by="Rating", ascending=False)
    return results.head(20).to_dict(orient="records")

# ---------------- FEATURED ----------------
@app.get("/featured")
def featured():
    return df.sample(20).to_dict(orient="records")

# ---------------- RECOMMEND ----------------
@app.get("/recommend/{product_id}")
def recommend(product_id: int):
    results = recommend_products(product_id)
    return {"recommended_products": results}