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


def get_words_list(lyric: str, mode: int = 1) -> list:
    word_list = word_tokenize(lyric)
    if(mode == 1):
        remove_list = ["'s", "n't", "'m", "'re", "'ll", "'ve", "'d", "'ll"]
        return [x for x in word_list if x not in remove_list]
    else:
        return word_list



def remove_stopwords(words: list) -> list:
    stoplist = stopwords.words('english')
    return [w for w in words if w not in stoplist]


def remove_punctuation(words: list) -> list:
    punctuation = set(string.punctuation)
    custom_punctuation = set(["...", "''", "'", "`", "``"])
    punctuation = punctuation.union(custom_punctuation)
    return [w for w in words if  w not in punctuation]


def preprocess(lyric: str, mode: int = 1) -> list:
    lyric = lyric.lower()
    lyric = lyric.replace("\r", '\n')
    lyric = lyric.replace("\r\n", '\n')
    lyric = lyric.replace("\r\n", '\n')
    
    lyric = lyric.replace("can't", 'can not')
    lyric = lyric.replace("won't", 'will not')
    lyric = lyric.replace("gonna", 'going to')
    lyric = lyric.replace("wanna", 'want to')
    lyric = lyric.replace("gotta", 'got to')
    lyric = lyric.replace("'cause", 'because')
    lyric = lyric.replace("'bout", 'about')
    
    lyric = lyric.replace("'ll", ' will')
    lyric = lyric.replace("'ve", ' have')
    lyric = lyric.replace("n't", ' not')
    lyric = lyric.replace("'m", ' am')
    lyric = lyric.replace("'re", ' are')
    
    words = get_words_list(lyric, mode)
    if(mode == 1):
        words = remove_stopwords(words) # i, you, me...

    words = remove_punctuation(words)
    return words

