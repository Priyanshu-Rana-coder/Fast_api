from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCEHMY_DATABASE_URL=SQLALCHEMY_DATABASE_URL = "postgresql://postgres:prash741@localhost/FastAPi"

engine=create_engine(SQLALCEHMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()