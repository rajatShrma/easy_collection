from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import  Session, select
from database import get_session
from schemas.product import  ProductCreateModel, ProductReadModel,UpdateProductModel
from models.product import Product

router = APIRouter(prefix= "/product", tags=["Product"])
sessionDep = Annotated[Session, Depends(get_session)]

@router.post("/add", response_model =ProductReadModel)
def create_product(product_data:ProductCreateModel, session:sessionDep):
    product_context = Product(
    name = product_data.name,
    company = product_data.company,
    description= product_data.description,
    price= product_data.price, 
    expiry_date = product_data.expiry_date 
)
    session.add(product_context)
    session.commit()
    session.refresh(product_context)
    return product_context

@router.get("/list", response_model = list[ProductReadModel])
def get_product(session:sessionDep):
    product_list = session.exec(select(Product)).all()
    return product_list


@router.put("/update/id")
def update_product(id: int, brand_update: UpdateProductModel,session:sessionDep):
    product_context = session.get(Product,id)
    if not product_context:
        raise HTTPException(status_code=404, detail="requested product not found")
    for key, value in brand_update.dict(exclude_unset=True).items():
        setattr(product_context,key,value)

    session.add(product_context)
    session.commit()
    session.refresh(product_context)
    return product_context   

@router.delete("/delete/{id}")
def delete_product(id: int, session:sessionDep):
    Product_context = session.get(Product, id)
    if not Product_context:
        raise HTTPException(status_code=404, detail= "requested product not found")
    session.delete(Product_context)
    session.commit()
    return{"message": "Product is successfully deleted"}


        

    