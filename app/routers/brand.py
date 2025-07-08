from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session,select
from database import get_session
from typing import Annotated
from schemas.brand import BrandCreate, BrandRead, UpdateBrandModel
from models.brand import Brand

router = APIRouter(prefix="/brand", tags=["Brand"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/add", response_model=BrandRead)
def create_brand(brand_data: BrandCreate, session: SessionDep):
    brand_context = Brand(
        name = brand_data.name,
        origin_country = brand_data.origin_country,
        description = brand_data.description,
        established_year = brand_data.established_year,
        is_active = brand_data.is_active   
    )
    session.add(brand_context)
    session.commit()
    session.refresh(brand_context)
    return brand_context


@router.get("/list", response_model = list[BrandRead])
def get_brand(session: SessionDep):
    brand_list = session.exec(select(Brand)).all()
    return brand_list


@router.put("/update/id")
def update_brand(id: int,update_brand: UpdateBrandModel, session:SessionDep):
    brand_context = session.get(Brand,id)
    if not brand_context:
        raise HTTPException(status_code=404, detail="requested brand not found")
    for key, value in update_brand.dict(exclude_unset=True).items():
        setattr(brand_context,key,value)

    session.add(brand_context)
    session.commit()
    session.refresh(brand_context)
    return brand_context
    

@router.delete("/delete/{id}")
def delete_brand(id: int,session:SessionDep):
    brand_context = session.get(Brand, id)
    if not brand_context:
        raise HTTPException(status_code=404, detail= "brand not found")
    session.delete(brand_context)
    session.commit()
    return{"message": "brand is successfully deleted"}

@router.get("/detail/{id}", response_model=BrandRead)
def brand_detail(id: int, session:SessionDep):
    brand_context = session.get(Brand, id)
    if not brand_context:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand_context