from app import app, db
from sqlalchemy import inspect

with app.app_context():
    print("DATABASE:", db.engine.url)

    tables = inspect(db.engine).get_table_names()

    print("\nTABLES:")
    for table in tables:
        print(" -", table)
