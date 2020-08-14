from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def connect_db():
    connection_string = "postgresql://postgres:489bb@localhost:5432/myshop"
    db = create_engine(connection_string)
    Session = sessionmaker(bind=db)
    db_session = Session()
    return db_session
