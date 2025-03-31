from fastapi import FastAPI, HTTPException, Depends, Request, status
from pydantic import BaseModel, datetime_parse
from typing import Annotated
from erikas import engine, SessionLocal
from sqlalchemy.orm import Session
import datetime
import models
import asyncio
from classes import Client
from database import db_query, connection
import datetime


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class UserBase(BaseModel):
    client_id: int
    username: str
    password: str


class TransactionBase(BaseModel):
    transaction_id: str
    username: str
    amount: int
    date: datetime.date
    transaction_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]




def make_transaction(username, password, amount: int, db: db_dependency):
    user = db.query(models.User).filter_by(username=username, password=password).first()
    while user is None:
        return "nezjbys"
    if amount > 0:
        transaction_type = "Deposit"
    elif amount < 0:
        transaction_type = "Withdrawal"
    transaction = models.Transaction(username=username, amount=amount, date=date_now, transaction_type=transaction_type)
    db.add(transaction)
    db.commit()



def create_user(username, password):
    client_id = 1
    while True:
        try:
            add_account_query = "INSERT INTO users (client_id, username, password) VALUES (%s, %s, %s)"
            account_data = (client_id, username, password)
            db_query(connection, add_account_query, account_data)
            connection.commit()
            break
        except Exception as e:
            print(e)
            client_id += 1

username = "awegawegaweg"
password = "awgwegawegsdfdf"

create_user(username, password)

@app.get("/users/", status_code=status.HTTP_200_OK)
async def read_user(db: db_dependency):
    user = db.query(models.User).all()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# @app.post("/posts/", status_code=status.HTTP_201_CREATED)
# async def make_deposit(post: TransactionBase, db: db_dependency):
#
#     deposit = models.User(**post.dict())
#     db.add(deposit)
#     db.commit()
