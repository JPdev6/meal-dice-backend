from sqlalchemy.orm import Session
from models import Meal

def get_meals(db: Session):
    return db.query(Meal).all()

def add_meal(db: Session, name: str):
    meal = Meal(name=name)
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return meal

def delete_meal(db: Session, meal_id: int):
    meal = db.query(Meal).filter(Meal.id == meal_id).first()
    if meal:
        db.delete(meal)
        db.commit()
        return True
    return False
