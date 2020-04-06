from nltk.tokenize import word_tokenize # TODO comprobar otro tokenizadores
from nltk.corpus import stopwords
import string
from collections import Counter

BIGRAMS_MODE = "bigrams"
UNIGRAMS_MODE = "unigrams"

def open_lyric_from_path(file_path: str) -> str:
    with open(file_path) as f:
        return f.read()


def open_lyric_from_index(index: str) -> str:
    try:
        f = open('./lyrics_lyricwikia/' + index)
        return f.read()
    except FileNotFoundError:
        return None


def get_words_list(lyric: str) -> list:
    return word_tokenize(lyric)


def remove_stopwords(words: list) -> list:
    stoplist = stopwords.words('english')
    return [w for w in words if w not in stoplist]


def remove_punctuation(words: list) -> list:
    punctuation = set(string.punctuation)
    return [w for w in words if  w not in punctuation]


def preprocess(lyric: str, mode: str) -> list:
    lyric = lyric.lower()
    lyric = lyric.replace("\r", '\n')
    lyric = lyric.replace("\r\n", '\n')
    lyric = lyric.replace("\r\n", '\n')
    words = get_words_list(lyric)
    if(mode == UNIGRAMS_MODE):
        words = remove_stopwords(words) # i, you, me...
    clean_words = remove_punctuation(words)
    return clean_words

