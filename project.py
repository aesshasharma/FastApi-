from fastapi import FastAPI, Response # response for created error no (201)
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Product(BaseModel):
    id : Optional[int] = None
    name:str
    price:float
    description: str

products = []
id = 0


@app.post("/products")
def create_product(product:Product,response:Response):
    global id
    try:
        id += 1
        product.id = id
        products.append(product)
        response.status_code = 201
        return{"isSuccess":True ,"message":"Product Created successfully","product":product}
    except Exception as e:
        print(e)
        response.status_code = 500
        return {"message":str(e),"isSuccess":False }


@app.get("/products")
def get_product(response:Response):
    try:
        response.status_code = 200
        return {"product":products,"isSuccess": True}
    except Exception as e:
        response.status_code = 500
        return {"message":"Error fetching products","isSuccess":False}
    
@app.get("/products/{productid}")
def get_product(productid:int, response:Response):
    try:
        response.status_code = 200
        for product in products:
            if product.id == productid:
                return {"product":product,"isSuccess": True}
        response.status_code = 404
        return {"message": "Product not found", "isSuccess": False}
    except Exception as e:
        response.status_code = 500
        return {"message":"Error fetching products","isSuccess":False}

# update
@app.put("/product/{productid}")
def updateProduct(productid: int, product: Product, response: Response):
    try:
        for index in range(len(products)):
            if products[index].id == productid:
                products[index] = product
                response.status_code = 200
                return {
                    "message": "Product updated successfully",
                    "isSuccess": True
                }

        response.status_code = 404
        return {
            "message": "Product not found",
            "isSuccess": False
        }

    except Exception as e:
        response.status_code = 500
        return {
            "message": "Error updating product",
            "isSuccess": False
        }
            