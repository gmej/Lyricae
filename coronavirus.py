from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd
import numpy as np
import re #Regular expression operations

import time, string

LIMIT = 6

def open_lyric(file_path):
    with open(file_path) as f:
        return f.read()


def get_words(lyric):
    return word_tokenize(lyric)


def remove_stopwords(words):
    stoplist = stopwords.words('english')
    return [w for w in words if w not in stoplist]


def remove_punctuation(words):
    punctuation = set(string.punctuation)
    return [w for w in words if  w not in punctuation]


def preprocess(lyric):
    lyric = lyric.lower()
    lyric = lyric.replace("\r", '\n')
    lyric = lyric.replace("\r\n", '\n')
    lyric = lyric.replace("\r\n", '\n')
    words = get_words(lyric)
    words = remove_stopwords(words) # i, you, me...
    clean_words = remove_punctuation(words)
    return clean_words


def get_lyric(index):
    with open('./lyrics_lyricwikia/' + index) as f:
        return f.read()


def get_csv_df():    
    csv_df = pd.read_csv('./datasets/MoodyLyrics.csv', 
                         na_values=['.'])
    return csv_df.head(LIMIT)


def read_all_lyrics(df):
    df.index += 1
    lyrics = [preprocess(get_lyric("ML" + str(i))) for i in range(1, LIMIT + 1)]
    flat_list = [item for sublist in lyrics for item in sublist]
    counter = Counter(flat_list).most_common()
    print(type(counter))
    print(counter[0])
    print(counter[1])
    
    df.insert(3, "Lyric", lyrics, True)
    
    happy_df = df[df['Emotion'] == 'happy']
    sad_df = df[df['Emotion'] == 'sad']
    relaxed_df = df[df['Emotion'] == 'relaxed']
    angry_df = df[df['Emotion'] == 'angry']
    print(happy_df)
    happy_counters = happy_df["Lyric"]
    #counter = Counter(dict(happy_counters))
    #for counter in happy_counters:


df = get_csv_df()
read_all_lyrics(df)
