from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class BookBase(BaseModel):
    title: str
    publication_date: date
    author_id: int
    metadata: Optional[dict] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    publication_date: Optional[date] = None
    author_id: Optional[int] = None
    metadata: Optional[dict] = None

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True

class AuthorBase(BaseModel):
    name: str

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    name: Optional[str] = None

class Author(AuthorBase):
    id: int
    books: List[Book] = Field(default_factory=list)

    class Config:
        orm_mode = True


class BookCount(BaseModel):
    author_name: str
    book_count: int

    class Config:
        orm_mode = False