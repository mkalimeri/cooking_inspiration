import logging
from pathlib import Path
import json
import time

from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


def get_recipes(driver, link, recipes_dict):
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
            recipes_dict[name] = {"url": url, "ingredients": get_ingredients(page)}

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
            time.sleep(5)


def get_ingredients(page):
    ingredients = [
        str(ingredient.contents[0])
        for ingredient in BeautifulSoup(page.text, "html.parser").find_all("td", class_=None)
    ]
    # class_=None because we don't want to retrieve the measurements
    return ingredients


def scrape_urls(links, jsn_file):
    # If the json file exists, we do not get the data from the website again
    if jsn_file.exists():
        logging.info("Data has already been downloaded")
        logging.info("Downloading json file")
        with open(jsn_file, "rb") as f:
            all_recipes_dict = json.load(f)
    # If not, get the data from the website
    else:
        all_recipes_dict = {}

        # Installing webdriver
        logging.info("Installing Chrome webdriver")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # load the web page
        for link in links:
            get_recipes(driver, link, all_recipes_dict)

        driver.quit()
        logging.info("Finished! ")
        with open(jsn_file, "w") as f:
            json.dump(all_recipes_dict, f)

    return all_recipes_dict


if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent.parent.parent

    # URL of the website to scrape
    links = [
        "https://ottolenghi.co.uk//pages/mains-recipes",
        'https://ottolenghi.co.uk/pages/sides-recipes',
        'https://ottolenghi.co.uk/pages/soup-recipes',
        'https://ottolenghi.co.uk/pages/salad-recipes',
    ]

    jsn_file = Path(BASE_DIR) / "data/interim/ottolenghi_recipes.json"

    all_recipes_dict = scrape_urls(links, jsn_file)
