from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:prash741@localhost:5432/FastAPi"

engine = create_engine(DATABASE_URL)

conn = engine.connect()

print("Connected Successfully!")