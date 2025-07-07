from fastapi import FastAPI, Depends
import schemas
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:2500",
    "https://shopping-list-fe.onrender.com"
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Your list of allowed origins
    allow_credentials=True, # Set to True to allow credentials (cookies, authorization headers)
    allow_methods=["*"],    # Allows all methods (or specify specific methods like ["GET", "POST"])
    allow_headers=["*"],    # Allows all headers (or specify specific headers)
)

Base.metadata.create_all(engine)
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# fakeDatabase = {
#     1: {"item": "shoes"},
#     2: {"item": "book"},
#     3: {"item": "makeup"}
# }

@app.get("/")
def getItems(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items

@app.get("/{id}")
def getItem(id:int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item

@app.post("/")
def addItem(item:schemas.Item, session = Depends(get_session)):
    item = models.Item(task = item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.put("/{id}")
def updateItem(id:int, item:schemas.Item, session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject

@app.delete("/{id}")
def deleteItem(id:int, session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'Item was deleted'


