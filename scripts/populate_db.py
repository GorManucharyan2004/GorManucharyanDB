import requests
from datetime import datetime
import random

API_URL = "http://127.0.0.1:8000"

authors = [
    "J.K. Rowling",
    "George R.R. Martin",
    "J.R.R. Tolkien",
    "Agatha Christie",
    "Stephen King",
]

titles = [
    "Harry Potter and the Philosopher's Stone",
    "A Game of Thrones",
    "The Hobbit",
    "Murder on the Orient Express",
    "The Shining",
]

metadata_samples = [
    {"genre": "Fantasy"},
    {"genre": "Mystery"},
    {"genre": "Horror"},
    {"genre": "Science Fiction"},
    {"genre": "Adventure"},
]

def create_authors():
    author_ids = []
    for name in authors:
        response = requests.post(f"{API_URL}/authors/", json={"name": name})
        if response.status_code == 200:
            author = response.json()
            author_ids.append(author['id'])
        else:
            print(f"Failed to create author {name}: {response.text}")
    return author_ids

def create_books(author_ids):
    for _ in range(100):
        title = random.choice(titles) + f" {random.randint(1,1000)}"
        publication_date = datetime.strptime(f"{random.randint(1950,2023)}-{random.randint(1,12)}-{random.randint(1,28)}", "%Y-%m-%d").date()
        author_id = random.choice(author_ids)
        metadata = random.choice(metadata_samples)
        book_data = {
            "title": title,
            "publication_date": publication_date.isoformat(),
            "author_id": author_id,
            "metadata": metadata
        }
        response = requests.post(f"{API_URL}/books/", json=book_data)
        if response.status_code != 200:
            print(f"Failed to create book {title}: {response.text}")

if __name__ == "__main__":
    author_ids = create_authors()
    create_books(author_ids)
