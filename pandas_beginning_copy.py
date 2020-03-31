from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd
import numpy as np
import re #Regular expression operations
import os
import time, string

#NUMBER_OF_SONGS = len(os.listdir('./lyrics_lyricwikia/'))
NUMBER_OF_SONGS = 100

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
    try:
        f = open('./lyrics_lyricwikia/' + index)
        return f.read()
    except FileNotFoundError:
        return None


def get_csv_df():    
    csv_df = pd.read_csv('./datasets/MoodyLyrics.csv', 
                         na_values=['.'])
    return csv_df.head(NUMBER_OF_SONGS)


def insert_lyrics_to_df(df):
    df.index += 1 # Start index = 1
    lyrics = []
    for i in range(1, NUMBER_OF_SONGS + 1):
        lyric = get_lyric("ML" + str(i))
        if(lyric):
            lyric = preprocess(lyric)
            #print(lyric)
        lyrics.append(lyric)
    print("TOTAL SONGS: ", len(lyrics))
    
    df.insert(3, "Lyric", lyrics, True)

    return df

def word_bags(df: pd.DataFrame, emotion):
    
    """ 
    sad_df = df[df['Emotion'] == 'sad']
    sad_list = [item for sublist in sad_df['Lyric'].tolist() for item in sublist]
    relaxed_df = df[df['Emotion'] == 'relaxed']
    relaxed_list = [item for sublist in relaxed_df['Lyric'].tolist() for item in sublist]
    angry_df = df[df['Emotion'] == 'angry']
    angry_list = [item for sublist in angry_df['Lyric'].tolist() for item in sublist]
    """
    
    emotion_df = df[df['Emotion'] == emotion]
    word_list = [item for sublist in emotion_df['Lyric'].tolist() for item in sublist] 
    counter = Counter()
    counter.update(word_list)
    counter = cut_bag(counter, 3)
    words_df = pd.DataFrame(columns= ["Word", "TotalRepetitions", "FileOcurrences"])
    print(words_df)
    print('TOTAL WORDS: ', len(counter))
    file_ocurrences = get_file_ocurrences(df, counter)
    print('-----------------------------')
    word_repetitions = []
    for word in counter:
        print(word)
        word_repetitions.append(counter[word])
    print ('file_ocurrences: ', file_ocurrences)
    print ('word_repetitions: ', word_repetitions)
    print ('counter: ', counter)
    for i in range(len(file_ocurrences)):
        if(file_ocurrences[i] > word_repetitions[i]):
            print('MAL !!!!!!', file_ocurrences[i], word_repetitions[i] )
    for word in counter:
        #row = pd.Series([word, happy_counter[word], file_ocurrences])
        row = [word, counter[word], file_ocurrences]
        #happy_words_df = pd.concat([happy_words_df, row_df], ignore_index = True)
        #happy_words_df.loc[]
        #print("FILE OCURRENCES:",word,happy_counter[word], file_ocurrences)
    #print(happy_counter)
    get_weights(counter)


def cut_bag(bag: Counter, minimum_repetitions: int):
    return Counter(el for el in bag.elements() if bag[el] >= minimum_repetitions)

def get_file_ocurrences(df: pd.DataFrame, counter: Counter): # da positivo buscar 'A' en 'holA'. MALMALMALMALMAL
    list_of_lyrics = df['Lyric'].tolist()
    ocurrences = []
    for word in counter:
        #print(word)
        
        n = 0
        for file in list_of_lyrics:
            #print('word: ', word)
            for w in file:
                if(word == w):
                    #print('???''??''??''')
                    n += 1
                    break;
        ocurrences.append(n)
        #exit()
    return ocurrences

def get_weights(counter):
    word_repetitions_tuple = counter[0]
    #for word in counter.most_common():
        #print(word[0], word[1])
    
    
    
df = get_csv_df()
df = insert_lyrics_to_df(df)
word_bags(df, 'relaxed')
