from shop.db_connection import connect_db
from sqlalchemy import Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

db = connect_db()


class Buyer(Base):
    __tablename__ = 'buyers'
    buyer_id = Column(Integer, primary_key=True)
    buyer_name = Column(String(30), unique=False, nullable=False)
    mail_id = Column(String(120), unique=True, nullable=False)
    phone_no = Column(String(15), unique=True, nullable=False)
    password = Column(String(20), unique=True, nullable=False)


def save_user(buyer_name, mail_id, phone_no, password):
    print(buyer_name, mail_id, phone_no, password)
    obj = Buyer(buyer_name=buyer_name, mail_id=mail_id, phone_no=phone_no, password=password)
    db.add(obj)
    db.commit()
    return 'true'


def is_user_exists(mail_id, password):
    buyer = db.query(Buyer).filter_by(mail_id=mail_id, password=password).first()
    if buyer:
        return 'true', buyer.buyer_id, buyer.buyer_name
    else:
        return 'false', None, None