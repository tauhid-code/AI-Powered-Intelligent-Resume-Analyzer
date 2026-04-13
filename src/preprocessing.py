"""
This file is responsible for all text cleaning and normalization operations to both resume and job description before extraction.
It also handles lowercasing, special character removal, stopword filtering, and whitespace normalization.
"""

import re 
import logging 
from typing import Optional 

logger = logging.getLogger(__name__)

## to preserve words meaning, so that they are not changed while applying stop words.

_KEEP_WORDS = {"not", "no", "c", "r"}

def load_stopwords() -> set[str]:
    """
    Load english stopwords from NLTK  and download the corpus automatically if not already present.
    """
    try:
        import nltk 
        from nltk.corpus import stopwords 

        try:
            words = set(stopwords.words("english")) 
        except LookupError:
            logger.info("NLTK stopwords corpus not found. Downloading now...")
            nltk.download("stopwords",quiet=True)
            words = set(stopwords.words("english"))
        return words

    except ImportError:
        logger.warning("NLTK library is not installed. Please install it using 'pip install nltk' to use stopword filtering.")

        return set()
    
def get_stopwords() -> set[str]:
    """
    Get the set of stopwords, excluding the words in _KEEP_WORDS.
    """
    stop_words = load_stopwords()
    filtered_stop_words = stop_words - _KEEP_WORDS
    return filtered_stop_words 

def to_lowercase(text:str) -> str:
    """
    Convert the input text to lowercase.
    """
    return text.lower()

def remove_special_characters(text:str) -> str:
    """
    Remove special characters from the input text, keeping only alphanumeric characters and spaces.
    """
    text = re.sub(r'[^a-zA-Z0-9\s\+\=\.\-\/]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def remove_stopwords(text: str, stop_words: Optional[set[str]]=None) -> str:
    """
    Remove stopwords from the input text using the provided set of stopwords.
    If no set is provided, it will load the default stopwords.
    """
    if stop_words is None:
        stop_words = get_stopwords()
    
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

def normalize_whitespace(text: str)-> str: 
    """
    Multiple whitespaces replaced with a single space."""

    return re.sub(r"\s+", " ", text).strip()

def preprocess_text(text: str, remove_stops: bool = True) -> str:
    """
    Run full preprocessing pipeline on the full input text."""

    text = to_lowercase(text)
    text = remove_special_characters(text)
    if remove_stops:
        text = remove_stopwords(text)
    text = normalize_whitespace(text)
    return text

def tokenize(text: str) -> list[str]:
    """
    Split preprocessed text into a list of individual word tokens,q filtering noise tokens.
    """
    return [token for token in text.split() if len(token) > 1]