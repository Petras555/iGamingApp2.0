from sqlalchemy import Boolean, Column, Integer, String, DATETIME, ForeignKey
from erikas import Base

class User(Base):
    __tablename__ = 'users'

    client_id = Column(Integer, primary_key=True, default=None, unique=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True,)
    password = Column(String(50),)


# class Transaction(Base):
#     __tablename__ = 'transactions'

#     transaction_id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
#     username = Column(String(50), unique=True)
#     amount = Column(Integer)
#     date = Column(DATETIME)
#     transaction_type = Column(String(50))

class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), ForeignKey("users.username"))
    amount = Column(Integer, nullable=False)  # Ensure the column is defined
    date = Column(DATETIME, nullable=False)
    transaction_type = Column(String(50), nullable=False)