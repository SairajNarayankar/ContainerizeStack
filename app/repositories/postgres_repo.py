from sqlalchemy.orm import Session
from app.models import Item

class PostgresItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Item).all()

    def get_by_id(self, item_id: int):
        return self.db.query(Item).filter(Item.id == item_id).first()

    def create(self, name: str, description: str = None):
        item = Item(name=name, description=description)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item_id: int):
        item = self.get_by_id(item_id)
        if item:
            self.db.delete(item)
            self.db.commit()
        return item