from dataclasses import dataclass
from typing import List


@dataclass
class Recipe:
    name: str  # The name of the recipe
    url: str  # The url of the recipe
    ingredients: List[str]  # a list of ingredients

    def __eq__(self, other):
        # Two Recipe instances are equal if they have the same URL
        if self.url == other.url:
            return True
        return False

    def __str__(self):
        return self.name

    @classmethod
    def encode_recipe(cls, obj):
        # Encode a Recipe instance so it can be saved as a json dictionary
        if isinstance(obj, cls):
            return {"name": obj.name, "url": obj.url, "ingredients": obj.ingredients}
        return obj

    @classmethod
    def decode_recipe(cls, obj):
        # decode a json dictionary to get a Recipe instance
        if isinstance(obj, dict):
            return cls(name=obj["name"], url=obj["url"], ingredients=obj["ingredients"])
        return obj
