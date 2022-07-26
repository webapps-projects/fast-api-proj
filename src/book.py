from typing import Optional
from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()
books = {
    1: {

        "name": "The Enchanted Charms",
        "author_name": "Geronimo",
        "price": 250
    },
    2: {
        "name": "Diary of a Wimpy Kid",
        "author_name": "Jeff Kinney",
        "price": 350
    }
}


class Book(BaseModel):
    name: str
    author_name: str
    price: int


class UpdateBook(BaseModel):
    name: Optional[str] = None
    author_name: Optional[str] = None
    price: Optional[int] = None


@app.get("/")
def index():
    return {"task": "FastAPI Execution"}

# get book by using path param


@app.get("/get-book/{book_id}")
def get_book(book_id: int = Path(None, description="Book ID should be greater than 0 and less than 3", gt=0, le=3)):
    return books[book_id]

# get by using query params
# Make name as optional


@app.get("/get-by-name")
def get_book(*, name: Optional[str] = None, test: int):
    for book_id in books:
        if books[book_id]["name"] == name:
            return books[book_id]
    return {"Data": "Not found"}


# Combining Path and Query param
# to correct later the logic to fetch the correct details

@app.get("/get-by-name/{book_id}")
def get_by_name(*, name: Optional[str] = None, book_id: int):
    for id in books:
        if id == book_id or books[id]["name"] == name:
            return books[id]

    return {"Data": "Not found"}


@app.post("/create-a-book/{book_id}")
def create_book(book_id: int, book: Book):
    if book_id in books:
        return {"Error": "book already exists"}
    books[book_id] = book
    return books[book_id]


@app.put("/update-a-book/{book_id}")
def update_book(book_id: int, book: UpdateBook):
    if book_id not in books:
        return {"Error": "book does not exists"}
    
    if book.name != None:
        books[book_id].name = book.name
    if book.author_name!=None:
        books[book_id].author_name = book.author_name
    if book.price!=None:
        books[book_id].price = book.price

    return books[book_id]

@app.delete("/delete-book/{book_id}")
def delete_book(book_id:int):
    if book_id not in books:
        return {"Error": "book doesn't exists"}
    del books[book_id]
    return {"Messsage": "Book has been deleted succesfully"}
      
