from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import func

from . import models, schemas


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(db: Session, author_id: int, author: schemas.AuthorUpdate):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if db_author:
        for key, value in author.dict(exclude_unset=True).items():
            setattr(db_author, key, value)
        db.commit()
        db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if db_author:
        db.delete(db_author)
        db.commit()
    return db_author


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: schemas.BookUpdate):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        for key, value in book.dict(exclude_unset=True).items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book


def get_books_by_author_and_date(db: Session, author_id: int, publication_date: date):
    return db.query(models.Book).filter(
        models.Book.author_id == author_id,
        models.Book.publication_date == publication_date
    ).all()


def update_books_metadata_by_author(db: Session, author_id: int, new_metadata: dict):
    books = db.query(models.Book).filter(models.Book.author_id == author_id).all()
    for book in books:
        if book.metadata:
            book.metadata.update(new_metadata)
        else:
            book.metadata = new_metadata
    db.commit()
    return books


def get_book_counts_by_author(db: Session):
    return db.query(models.Author.name, func.count(models.Book.id)).join(models.Book).group_by(models.Author.id).all()