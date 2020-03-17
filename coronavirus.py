from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd
import numpy as np
import re #Regular expression operations

import time, string


def open_lyric(file_path):
    with open(file_path) as f:
        return f.read()

def get_words(lyric):
    return word_tokenize(lyric)

def remove_stopwords(words):
    stoplist = stopwords.words('english')
    #print(stoplist)
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
    print(words)
    #lemmas = lemmatize(words)
    words = remove_stopwords(words) # i, you, me...
    print(words)
    #before this i should use punctuation for something
    clean_words = remove_punctuation(words)
    print(clean_words)
    return clean_words

def get_lyric(index, artist, song, emotion):
    file_name = '_'.join([emotion, artist, song])
    file_name = file_name.replace('/', '-')  # The '/' should never appear
    file_name = file_name.replace(' ', '.') 
    with open('./lyrics_lyricwikia/' + file_name) as f:
        return f.read()
     
def pandas():
    words = re.findall(r'\w+', open(FILE).read().lower())
    counted_words = Counter(words).most_common()
    df = pd.DataFrame(counted_words, columns=['word', 'repetitions'])
    
    csv_df = pd.read_csv('./datasets/MoodyLyrics.csv', 
                         names=['Index','Artist', 'Song', 'Emotion'],
                         na_values=['.'])
    csv_df = csv_df.sort_values(by="Artist")
    #print(csv_df[csv_df['Song'].isin(['.'])]) # Check empty values. No one
    little_df = csv_df.head(10)
    print(little_df)
    for index, row in little_df.iterrows():
        #little_df.loc[little_df['Index'] == index, 'Lyric'] = get_lyric(index, row['Artist'], row['Song'], row['Emotion'])
        new_df = little_df[little_df['Index'] == 'ML'+ str(index)]
        print(index)
        new_df['Lyric'] = 'aaaa'
    print(little_df)
        
    





FILE = './lyrics_lyricwikia/angry_Marilyn.Manson_Sweet.Dreams.'
pandas()
#lyric = open_lyric('./lyrics_lyricwikia/angry_Marilyn.Manson_Sweet.Dreams.')
#print(lyric)

#preprocess(lyric)