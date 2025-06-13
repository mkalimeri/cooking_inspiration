import re
import string
from typing import List

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

from nltk.tokenize import word_tokenize

from .recipe import Recipe
from cooking_seasonally.helpers.utils import LIST_TO_IGNORE

def to_lower(txt: str) -> str:
    # Convert to lower
    return txt.lower()


def remove_characters(characters: str, txt: str) -> str:
    # Remove characters in 'characters' from txt
    translator = str.maketrans("", "", characters)
    return txt.translate(translator)


def tokenize(txt: str) -> List[str]:
    # Returns the indivisuals token words of a string
    return word_tokenize(txt)


def remove_blank(txt: str) -> str:
    # Removes leading and ending blank spaces from a string
    return txt.strip()


def remove_numbers(txt: str) -> str:
    # Removed digits from a string
    result = re.sub(r"\d+", "", txt)
    return result


def remove_stopwords(words_lst: List[str]) -> List[str]:
    # Removes predefined stopwords from list of words
    stop_words = set(stopwords.words("english"))
    filtered_text = [word for word in words_lst if word not in stop_words]
    return filtered_text


def lemmatize(words_lst: List[str]) -> List[str]:
    # retrieve the roots of words in a list by means of lemmatization
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in words_lst]


def stemming(words_lst: List[str]) -> List[str]:
    # retrieve the roots of words in a list by means of stemming (using PortStemmer)
    stemmer = PorterStemmer()
    return [stemmer.stem(word) for word in words_lst]


def ignore_item(list_to_ignore: List[str], words: str) -> bool:
    # Returns true is string 'words' contains one of the words in list_to_ignore
    for x in list_to_ignore:
        if x in words.split():
            return True
    return False

def remove_item_if_in_list(list_of_items: List[str], list_to_ignore: List[str]) -> List[str]:
    # Checks if item in list_of_items contains string from list_to_ignore and removes it, if it does
    return [item for item in list_of_items if not ignore_item(list_to_ignore, item)]


def preprocess_ingredients(words_lst: List[str]) -> List[str]:
    # Use the mothods defined above to proprocess a list of words

    # Order of processing per word in list: make lowercase, remove punctuation symbols, remove blank spaces, remove digits
    l = [
        remove_numbers(remove_blank(remove_characters(string.punctuation, to_lower(txt))))
        for txt in words_lst
    ]
    return list(filter(None, l))  # remove empty strings from list
    # tokens = [remove_stopwords(tokenize(txt)) for txt in l]  # Remove stopwords
    # return [stemming(lst) for lst in tokens]  # perform stemming