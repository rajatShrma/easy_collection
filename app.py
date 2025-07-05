from fastapi import FastAPI, Depends
from typing import Annotated
from fastapi_sqlmodel import DBSessionMiddleware, db
from sqlmodel import create_engine, SQLModel, Session, select
from fastapi import HTTPException


from user.models import User, UserCreateModel
from product.models import Product, ProductCreateModel
from brand.models import Brand, BrandBaseModel
from contactmessage.models import ContactMessage, ContactMessageModel, UpdateContactMessageModel


app = FastAPI()

sqlite_url = "sqlite:///./muna_collection_db.db"
app.add_middleware(DBSessionMiddleware, db_url=sqlite_url)

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/user/")
def create_user(user: UserCreateModel, session: SessionDep):
    user_context  = User(
        first_name = user.first_name,
        last_name = user.last_name,
        phone = user.phone,
        email = user.email,
        address = user.address,
        gender = user.gender
    )
    session.add(user_context)
    session.commit()
    session.refresh(user_context)
    return user_context


@app.get("/product")
def get_product(session: SessionDep):    
    Product_list = session.exec(select(Product)).all()
    return Product_list

@app.post("/product")
def create_product(product: ProductCreateModel, session: SessionDep):
    db_product  = Product(
        name = product.name,
        company = product.company,
        description = product.description,
        price = product.price,
        expiry_date = product.expiry_date
    )
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    print(type(db_product.price))
    return db_product

@app.get("/brand")
def get_brand(session: SessionDep):    
    brand_list = session.exec(select(Brand)).all()
    return brand_list


@app.post("/brand")
def create_brand(brand: BrandBaseModel, session: SessionDep):
    db_brand = Brand(
        name = brand.name,
        origin_country = brand.origin_country,
        description = brand.description,
        established_year = brand.established_year,
        is_active = brand.is_active
    )

    session.add(db_brand)
    session.commit()
    session.refresh(db_brand)
    return db_brand


@app.put("/brand/brand_id")
def update_brand(
    brand_id: int,
    update_brand: BrandBaseModel,
    session: SessionDep
):

    db_brand = session.get(Brand, brand_id)
    if not db_brand:
        raise HTTPException(status_code=404, detail="brand not found")
    brand_data = update_brand.model_dump(exclude_unset = True)
    db_brand.sqlmodel_update(brand_data)
    session.add(db_brand)
    session.commit()
    session.refresh(db_brand)
    return db_brand


@app.delete("/delete_brand/{id}")
def delete_brand(id: int, session: SessionDep):
    brand = session.get(Brand, id)
    if not brand:
        raise HTTPException(status_code=404, detail= "brand not found")
    session.delete(brand)
    session.commit()
    return{"ok": True}



@app.get("/contact_message")
def get_message(session: SessionDep):    
    ContactMessage_list = session.exec(select(ContactMessage)).all()
    return ContactMessage_list


@app.post("/contactmessage")
def add_contactmessage(contactmessage: ContactMessageModel, session: SessionDep):
    contactmessage_db = ContactMessage(
        full_name = contactmessage.full_name,
        email = contactmessage.email,
        subject = contactmessage.subject,
        message = contactmessage.message   
    )

    session.add(contactmessage_db)
    session.commit()
    session.refresh(contactmessage_db)
    return contactmessage_db


@app.put("/contactmessage/id")
def update_message(
    id: int,
    update_message: UpdateContactMessageModel,
    session: SessionDep
):

    contactmessage_db = session.get(ContactMessage, id)
    if not contactmessage_db:
        raise HTTPException(status_code=404, detail="message not found")
    for key, value in update_message.dict(exclude_unset= True).items():
        setattr(contactmessage_db, key, value)
    session.add(contactmessage_db)
    session.commit()
    session.refresh(contactmessage_db)
    return contactmessage_db


@app.delete("/delete_contactmessage/{id}")
def delete_message(id: int, session: SessionDep):
    contactmessaage = session.get(ContactMessage, id)
    if not contactmessaage:
        raise HTTPException(status_code=404, detail= "contactmessage not found")
    session.delete(contactmessaage)
    session.commit()
    return{"detail": "contact message successfully deleted"}

