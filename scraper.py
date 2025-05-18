import requests
from bs4 import BeautifulSoup
import wikipedia

def fetch_recipe_akis(meal):
    search_url = f"https://akispetretzikis.com/en/search?q={meal}"
    res = requests.get(search_url)
    soup = BeautifulSoup(res.text, "html.parser")

    # Get first result
    first = soup.select_one(".card__title a")
    if not first:
        return None

    link = "https://akispetretzikis.com" + first["href"]
    recipe_page = requests.get(link)
    recipe_soup = BeautifulSoup(recipe_page.text, "html.parser")

    title = recipe_soup.select_one("h1").text.strip()
    ingredients = [
        i.text.strip()
        for i in recipe_soup.select(".ingredients__list li")
    ]

    return {
        "title": title,
        "ingredients": ingredients,
        "url": link
    }

def fetch_wiki_summary(meal):
    try:
        return wikipedia.summary(meal, sentences=2)
    except:
        return "No Wikipedia summary found."

def fetch_reddit_links(meal):
    # Simulated: in production, use Reddit API
    return [
        {
            "title": f"Is {meal} healthy?",
            "url": f"https://www.reddit.com/search/?q={meal}+health"
        }
    ]
