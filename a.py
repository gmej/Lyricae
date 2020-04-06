INITIAL_NUMBER_OF_SONGS = 5000
from functions.lyrics_functions  import *
import pandas as pd
import os
LYRICS_DATASET_PATH = './datasets/MoodyLyrics.csv'
from nltk.corpus import stopwords
print(set(stopwords.words("english")))
exit()
import numpy as np

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




df = read_csv_as_df(LYRICS_DATASET_PATH)
print(df)
new_df = insert_lyrics_to_df(df)
print(new_df)