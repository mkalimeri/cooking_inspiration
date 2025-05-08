from pathlib import Path

from scrapping.get_recipes import scrape_url

if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent.parent

    # URL of the website to scrape

    links = {
        "mains": "https://ottolenghi.co.uk//pages/mains-recipes",
        "sides": "https://ottolenghi.co.uk/pages/sides-recipes",
        "soup": "https://ottolenghi.co.uk/pages/soup-recipes",
        "salad": "https://ottolenghi.co.uk/pages/salad-recipes",
    }

    for course, link in links.items():
        jsn_file = Path(BASE_DIR) / f"data/interim/ottolenghi_recipes_{course}.json"

        all_recipes_list = scrape_url(link, jsn_file)

    # TODO: Do I want to stem or lematize? Some ingredients need to be removed - eg. oil, salt, pepper, spices
