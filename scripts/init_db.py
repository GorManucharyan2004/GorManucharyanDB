from app.database import engine, Base
import os


def init_db():
    if os.path.exists("app/app.db"):
        print("Database already exists.")
    else:
        Base.metadata.create_all(bind=engine)
        print("Database created successfully.")


if __name__ == "__main__":
    init_db()
