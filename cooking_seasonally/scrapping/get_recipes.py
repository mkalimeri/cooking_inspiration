import logging
import json
from pathlib import Path
import time
from typing import List

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

from cooking_seasonally.helpers.recipe import Recipe


def get_recipes_from_web(driver: webdriver, link: str, recipe_list: List[Recipe | None]):
    # Retrieve recipe information from the webdriver
    # This method is specisc to the www.ottolenghi.com recipe pages

    next_page_exists = True

    print(f"Getting recipes from {link}")
    logging.info(f"Getting recipes from {link}")
    driver.get(link)

    # set maximum time to load the web page in seconds
    driver.implicitly_wait(10)

    while next_page_exists:
        # collect data that are within the id 'recipes-page'
        recipes_page = driver.find_element(By.ID, "recipes-page")
        # Get all the recipe links
        recipes = recipes_page.find_elements(By.CLASS_NAME, "c-recipe-grid__item")

        for recipe in recipes:
            name = recipe.find_element(By.TAG_NAME, "span").text
            url = recipe.get_attribute("href")
            page = requests.get(url)
            recipe_list.append(
                Recipe(name=name, url=url, ingredients=get_ingredients_from_web(page))
            )
        try:
            # Get "load more" button to get to the next page
            button = recipes_page.find_element(By.CLASS_NAME, "c-button")

        except NoSuchElementException:
            # We reached the last page, the "load more" button does not exist
            logging.info(f"Reached the last page of {link}")
            next_page_exists = False
            continue
        else:
            driver.execute_script("arguments[0].click();", button)
            time.sleep(15)


def get_ingredients_from_web(page: requests.Response) -> List[str]:
    # Retrieve the ingredients of a recipe on a static page
    # This method is specisc to the www.ottolenghi.com recipe pages
    ingredients = [
        str(ingredient.contents[0])
        for ingredient in BeautifulSoup(page.text, "html.parser").find_all("td", class_=None)
    ]
    # class_=None because we don't want to retrieve the measurements
    return ingredients


def scrape_url(link: str, jsn_file: str) -> List[Recipe]:
    # If the provided json file does not exist, scrap recipe information from a given page
    # Save this information in the provided json file

    # If the json file exists, we do not get the data from the website again
    if jsn_file.exists():
        logging.info("Data already exists")
        print(f"{jsn_file}: Data already exists, no action taken")
    # If not, get the data from the website
    else:
        # Installing webdriver
        logging.info("Installing Chrome webdriver")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # load the web page
        all_recipes_list = []
        get_recipes_from_web(driver, link, all_recipes_list)

        with open(jsn_file, "w") as f:
            json.dump(all_recipes_list, f, default=Recipe.encode_recipe)

        driver.quit()

        logging.info("Finished! ")

        return all_recipes_list

if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent.parent.parent

    # URL of the website to scrape

    links = {
        "mains": "https://ottolenghi.co.uk//pages/mains-recipes",
        "sides": "https://ottolenghi.co.uk/pages/sides-recipes",
        "soup": "https://ottolenghi.co.uk/pages/soup-recipes",
        "salad": "https://ottolenghi.co.uk/pages/salad-recipes",
    }

    for course, link in links.items():
        jsn_file = Path(BASE_DIR) / f"data/raw/ottolenghi_recipes_{course}.json"

        all_recipes_list = scrape_url(link, jsn_file)
