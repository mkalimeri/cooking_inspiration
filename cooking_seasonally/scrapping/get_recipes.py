import logging
from pathlib import Path
import pickle
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

    print(f'Getting recipes from {link}')
    logging.info(f'Getting recipes from {link}')
    driver.get(link)

    # set maximum time to load the web page in seconds
    driver.implicitly_wait(10)

    while next_page_exists:
        # collect data that are within the id 'recipes-page'
        recipes_page = driver.find_element(By.ID, 'recipes-page')
        # Get all the recipe links
        recipes = recipes_page.find_elements(By.CLASS_NAME, 'c-recipe-grid__item')

        for recipe in recipes:
            name = recipe.find_element(By.TAG_NAME, 'span').text
            url = recipe.get_attribute('href')
            recipes_dict[name] = {'url': url, 'ingredients': []}

        try:
            # Get "load more" button to get to the next page
            button = recipes_page.find_element(By.CLASS_NAME, 'c-button')

        except NoSuchElementException:
            # We reached the last page, the "load more" button does not exist
            logging.info(f'Reached the last page of {link}')
            next_page_exists = False
            continue

        else:
            driver.execute_script("arguments[0].click();", button)
            time.sleep(5)

def scrape_urls(links, pkl_file):
    # If the pickle file exists, we do not get the data from the website again
    if pkl_file.exists():
        logging.info('Data has already been downloaded')
        logging.info('Downloading pickle file')
        with open(pkl_file, 'rb') as f:
            all_recipes_dict = pickle.load(f)
    # If not, get the data from the website
    else:
        all_recipes_dict = {}

        # Installing webdriver
        logging.info('Installing Chrome webdriver')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # load the web page
        for link in links:
            get_recipes(driver, link, all_recipes_dict)

        driver.quit()
        logging.info('Finished! ')
        with open(pkl_file, 'wb') as fp:
            pickle.dump(all_recipes_dict, fp)

    return all_recipes_dict

if __name__ == '__main__':
    BASE_DIR = Path(__file__).parent.parent.parent

    # URL of the website to scrape
    links = [
        'https://ottolenghi.co.uk//pages/mains-recipes',
        'https://ottolenghi.co.uk/pages/sides-recipes',
        'https://ottolenghi.co.uk/pages/soup-recipes',
        'https://ottolenghi.co.uk/pages/salad-recipes',
        ]

    pkl_file = Path(BASE_DIR) / "data/interim/ottolenghi_recipes.pkl"
    all_recipes_dict = scrape_urls(links, pkl_file)
    # print(len(all_recipes_dict.items()))
    # print(all_recipes_dict.get('Hot yoghurt and broad bean soup'))
