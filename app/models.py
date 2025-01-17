from sqlalchemy import Column, Integer, String, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    birth_date = Column(Date, nullable=True)

    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("authors.id"))
    isbn = Column(String, unique=True, nullable=True, index=True)

    author = relationship("Author", back_populates="books")