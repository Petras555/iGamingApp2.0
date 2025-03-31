from fastapi import FastAPI, HTTPException, Depends, Request, status
from pydantic import BaseModel, datetime_parse
from typing import Annotated
from erikas import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import func
import datetime
import models
import asyncio

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


async def make_transaction(post: TransactionBase, db: db_dependency):
    db_transaction = models.Transaction(**post.dict())
    db.add(db_transaction)
    db.commit()


@app.post("/deposit/", status_code=status.HTTP_200_OK)
async def make_transaction(username, password, amount: int, db: db_dependency):
    user = db.query(models.User).filter_by(username=username, password=password).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Invalid username or password")
    if amount == 0:
        raise HTTPException(status_code=400, detail="Invalid deposit with 0 funds")
    if amount < 0:
        raise HTTPException(status_code=405,
                            detail="Invalid deposit with negative amount of funds, please use withdraw function")

    transaction_type = "Deposit"
    transaction = models.Transaction(username=username, amount=amount, date=date_now, transaction_type=transaction_type)
    db.add(transaction)
    db.commit()


@app.post("/withdraw/", status_code=status.HTTP_200_OK)
async def make_transaction(username, password, amount: int, db: db_dependency):
    user = db.query(models.User).filter_by(username=username, password=password).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Invalid username or password")
    if amount == 0:
        raise HTTPException(status_code=400, detail="Invalid withdrawal of 0 funds")
    if amount < 0:
        raise HTTPException(status_code=400,
                            detail="Invalid withdrawal of negative amount of funds, please enter positive amount")

    users = db.query(
        models.Transaction.username,
        func.sum(models.Transaction.amount).label('Balance')
    ).filter(
        models.Transaction.username == username
    ).all()

    users_dict = [{"username": user.username, "Balance": user.Balance} for user in users]

    if amount >= users_dict[0]["Balance"]:
        raise HTTPException(status_code=400, detail="Not enough funds in Balance")

    amount = -amount
    transaction_type = "Withdrawal"
    transaction = models.Transaction(username=username, amount=amount, date=date_now, transaction_type=transaction_type)
    db.add(transaction)
    db.commit()


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
def create_user(username, password, db: db_dependency):
    db_user = models.User(username=username, password=password)
    db.add(db_user)
    db.commit()


@app.get("/users/", status_code=status.HTTP_200_OK)
async def read_user(db: db_dependency):
    user = db.query(models.User).all()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/tasks/1", status_code=status.HTTP_200_OK)
async def users_with_3_deposits(db: db_dependency):
    users = db.query(
        models.Transaction.username,
        func.count(models.Transaction.transaction_id).label('deposit_count')
    ).filter(
        "Deposit" == models.Transaction.transaction_type
    ).group_by(
        models.Transaction.username
    ).having(
        func.count(models.Transaction.transaction_id) >= 3
    ).all()

    if not users:
        raise HTTPException(status_code=404, detail="User not found")

    # Convert SQLAlchemy objects to dictionaries
    users_dict = [{"username": user.username, "deposit_count": user.deposit_count} for user in users]

    return users_dict


@app.get("/tasks/2", status_code=status.HTTP_200_OK)
async def users_with_1_withdrawal(db: db_dependency):
    users = db.query(
        models.Transaction.username,
        func.count(models.Transaction.transaction_id).label('withdrawal_count')
    ).filter(
        "Withdrawal" == models.Transaction.transaction_type
    ).group_by(
        models.Transaction.username
    ).having(
        func.count(models.Transaction.transaction_id) == 1
    ).all()

    if not users:
        raise HTTPException(status_code=404, detail="User not found")

    # Convert SQLAlchemy objects to dictionaries
    users_dict = [{"username": user.username, "withdrawal_count": user.withdrawal_count} for user in users]

    return users_dict


@app.get("/tasks/3", status_code=status.HTTP_200_OK)
async def top_3_deposits(db: db_dependency):
    transaction = db.query(models.Transaction)
    sorted_transactions = sorted(transaction, key=lambda x: x.amount, reverse=True)
    if not sorted_transactions:
        raise HTTPException(status_code=404, detail="User not found")
    return sorted_transactions[0:3]


@app.get("/tasks/4", status_code=status.HTTP_200_OK)
async def all_deposits(db: db_dependency):
    users = db.query(models.User).all()
    transactions = db.query(models.Transaction).filter("Deposit" == models.Transaction.transaction_type).all()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")

    # Convert SQLAlchemy objects to dictionaries3
    users_dict = []
    for user in users:
        for transaction in transactions:
            users_dict.append({"client_id": user.client_id, "username": user.username, "deposit_date": transaction.date,
                               "deposit_amount": transaction.amount})

    return users_dict


@app.get("/tasks/5", status_code=status.HTTP_200_OK)
async def users_balances(db: db_dependency):
    users = db.query(
        models.Transaction.username,
        func.sum(models.Transaction.amount).label('Balance')
    ).group_by(
        models.Transaction.username
    ).all()

    if not users:
        raise HTTPException(status_code=404, detail="User not found")

    # Convert SQLAlchemy objects to dictionaries
    users_dict = [{"username": user.username, "Balance": user.Balance} for user in users]

    return users_dict



