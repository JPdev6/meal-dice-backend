from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import Base
import crud
from fastapi.middleware.cors import CORSMiddleware
from scraper import fetch_recipe_akis, fetch_wiki_summary, fetch_reddit_links


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow frontend (adjust for your domain later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/meals")
def read_meals(db: Session = Depends(get_db)):
    return crud.get_meals(db)

@app.post("/meals")
def create_meal(name: str, db: Session = Depends(get_db)):
    return crud.add_meal(db, name)

@app.delete("/meals/{meal_id}")
def remove_meal(meal_id: int, db: Session = Depends(get_db)):
    success = crud.delete_meal(db, meal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Meal not found")
    return {"success": True}

@app.get("/fetch-info")
def fetch_info(meal: str):
    recipe = fetch_recipe_akis(meal)
    if not recipe:
        return {"error": "No recipe found for this meal."}

    return {
        "title": recipe["title"],
        "ingredients": recipe["ingredients"],
        "url": recipe["url"],
        "wikipedia_summary": fetch_wiki_summary(meal),
        "reddit_results": fetch_reddit_links(meal)
    }