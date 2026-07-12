from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.repositories.postgres_repo import PostgresItemRepository

Base.metadata.create_all(bind=engine)  # safety net

app = FastAPI()

@app.get("/items")
def list_items(db: Session = Depends(get_db)):
    repo = PostgresItemRepository(db)
    return repo.get_all()

@app.post("/items")
def create_item(name: str, description: str = None, db: Session = Depends(get_db)):
    repo = PostgresItemRepository(db)
    return repo.create(name, description)

@app.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    repo = PostgresItemRepository(db)
    return repo.get_by_id(item_id)