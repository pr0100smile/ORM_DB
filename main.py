import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
import datetime
from models import create_tables, get_shops, Publisher, Book, Shop, Stock, Sale


SQLsys = 'postgresql'
login = 'LOGIN'
password = 'PASSWORD'
host = 'localhost'
port = 5432
name_db = 'NAME DB'

DSN = f'{SQLsys}+psycopg2://{login}:{password}@{host}:{port}/{name_db}'
engine = sq.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

pub1 = Publisher(name='Пушкин', books=[
    Book(title="Капитанская дочка"),
    Book(title="Зимнее утро"),
    Book(title="Полтава"),
    Book(title="Сказка о царе Салтане")])

pub2 = Publisher(name='Лермонтов', books=[
    Book(title="Герой нашего времени"),
    Book(title="Мцыри"),
    Book(title="Маскарад"),
    Book(title="Пророк")])

pub3 = Publisher(name='Толстой', books=[
    Book(title="Война и мир"),
    Book(title="Анна Каренина"),
    Book(title="Воскресение"),
    Book(title="После бала")])

book1 = Book(title="Руслан и Людмила", publisher=pub1)
book2 = Book(title="Смерть поэта", publisher=pub2)
book3 = Book(title="Детство", publisher=pub3)

shop1 = Shop(name="Читай-Город")
stock1 = Stock(book=book1, shop=shop1, count=24)
sale1 = Sale(price=550, date_sale=datetime.datetime(2023, 10, 20), stock=stock1, count=43)
stock2 = Stock(book=book2, shop=shop1, count=15)
sale2 = Sale(price=645, date_sale=datetime.datetime(2023, 10, 22), stock=stock2, count=21)

shop2 = Shop(name="Буквоед")
stock3 = Stock(book=book2, shop=shop2, count=48)
sale3 = Sale(price=335, date_sale=datetime.datetime(2023, 10, 25), stock=stock3, count=35)
stock4 = Stock(book=book3, shop=shop2, count=56)
sale4 = Sale(price=555, date_sale=datetime.datetime(2023, 10, 27), stock=stock4, count=12)

session.add_all([pub1, pub2, pub3, shop1, shop2, stock1, stock2, stock3, stock4, sale1, sale2, sale3, sale4])
session.commit()


if __name__ == '__main__':
    pubs = input("Please enter a publisher name/id: ")
    get_shops(session, pubs)
    session.close()
