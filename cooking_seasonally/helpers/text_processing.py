import re
import string
from typing import List

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

from nltk.tokenize import word_tokenize

from .recipe import Recipe


def to_lower(txt: str) -> str:
    # Convert
    return txt.lower()


def remove_characters(characters: str, txt: str) -> str:
    # Remove characters in characters from txt
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


def preprocess_ingredients(words_lst: List[str]) -> List[str]:
    # Use the mothods defined above to proprocess a list of words (use stemming)

    # Order of processing per word in list: make lowercase, remove punctuation symbols, remove blank spaces, remove digits
    l = [
        remove_numbers(remove_blank(remove_characters(string.punctuation, to_lower(txt))))
        for txt in words_lst
    ]  # remove empty spaces and punctuation
    l = list(filter(None, l))  # remove empty strings from list
    tokens = [remove_stopwords(tokenize(txt)) for txt in l]  # Remove stopwords
    return [stemming(lst) for lst in tokens]  # perform stemming
