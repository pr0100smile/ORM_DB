import sqlalchemy as sq
from sqlalchemy import MetaData, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
metadata = MetaData()

class Publisher(Base):
    __tablename__ = 'publishers'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, unique=True)
    def __repr__(self):
        return f"Publisher (id={self.id}, name={self.name})"

class Book(Base):
    __tablename__ = 'books'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey('publishers.id'), nullable=False)

    publisher = relationship("Publisher", backref="books")

class Shop(Base):
    __tablename__ = 'shops'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, unique=True)
    def __repr__(self):
        return f"Shop (id={self.id}, name={self.name})"

class Stock(Base):
    __tablename__ = 'stocks'
    id = sq.Column(sq.Integer, primary_key=True)
    book_id = sq.Column(sq.Integer, sq.ForeignKey('books.id'), nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey('shops.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship("Book", backref="stocks")
    shop = relationship("Shop", backref="stocks")
    sales = relationship("Sale", backref="stock")

class Sale(Base):
    __tablename__ = 'sales'
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey('stocks.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def get_shops(db_session, pubs):
    result = db_session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).select_from(Shop). \
        join(Stock). \
        join(Book). \
        join(Publisher). \
        join(Sale)
    if pubs.isdigit():
        query = result.filter(Publisher.id == pubs).all()
    else:
        query = result.filter(Publisher.name == pubs).all()
    for Book.title, Shop.name, Sale.price, Sale.date_sale in query:
        print(f"{Book.title: <40} | {Shop.name: <10} | {Sale.price: <8} | {Sale.date_sale.strftime('%d-%m-%Y')}")