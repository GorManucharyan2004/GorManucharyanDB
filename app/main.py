import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from sqlalchemy.orm import joinedload

from app import models, schemas, crud
from app.database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.create_author(db, author)
    return db_author


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author: schemas.AuthorUpdate, db: Session = Depends(get_db)):
    db_author = crud.update_author(db, author_id, author)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.delete("/authors/{author_id}", response_model=schemas.Author)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.delete_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.create_book(db, book)
    return db_book


@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, sort_by: str = "title", db: Session = Depends(get_db)):
    query = db.query(models.Book)
    if sort_by == "publication_date":
        query = query.order_by(models.Book.publication_date)
    else:
        query = query.order_by(models.Book.title)
    books = query.offset(skip).limit(limit).all()
    return books


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = crud.update_book(db, book_id, book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.delete_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.get("/books/search/", response_model=List[schemas.Book])
def search_books(author_id: int, publication_date: date, db: Session = Depends(get_db)):
    books = crud.get_books_by_author_and_date(db, author_id, publication_date)
    return books


@app.get("/books_with_authors/", response_model=List[schemas.Book])
def get_books_with_authors(db: Session = Depends(get_db)):
    books = db.query(models.Book).options(joinedload(models.Book.author)).all()
    return books


@app.put("/books/update_metadata/", response_model=List[schemas.Book])
def update_books_metadata(author_id: int, new_metadata: dict, db: Session = Depends(get_db)):
    books = crud.update_books_metadata_by_author(db, author_id, new_metadata)
    return books


@app.get("/books/count_by_author/", response_model=List[schemas.BookCount])
def count_books_by_author(db: Session = Depends(get_db)):
    counts = crud.get_book_counts_by_author(db)
    return [{"author_name": name, "book_count": count} for name, count in counts]


@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, sort_by: str = "title", db: Session = Depends(get_db)):
    query = db.query(models.Book)
    if sort_by == "publication_date":
        query = query.order_by(models.Book.publication_date)
    else:
        query = query.order_by(models.Book.title)
    books = query.offset(skip).limit(limit).all()
    return books


@app.get("/books/search_metadata/", response_model=List[schemas.Book])
def search_books_metadata(query: str, db: Session = Depends(get_db)):
    books = crud.search_books_metadata(db, query)
    return books


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
