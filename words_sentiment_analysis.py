from nltk.util import bigrams
import pandas as pd
import numpy as np
import os
import time
import string
from functions.lyrics_functions import *


#NUMBER_OF_SONGS = len(os.listdir('./lyrics_lyricwikia/'))
INITIAL_NUMBER_OF_SONGS = 5000
MINIMUM_WORD_REPETITION = 50
MINIMUM_BIGRAM_REPETITION = 50
FINAL_NUMBER_OF_SONGS = INITIAL_NUMBER_OF_SONGS

LYRICS_DATASET_PATH = './datasets/MoodyLyrics.csv'

def read_csv_as_df(path: str) -> pd.DataFrame:    
    csv_df = pd.read_csv(path, na_values=['.'])
    return csv_df.head(INITIAL_NUMBER_OF_SONGS)


def insert_column_to_df(df: pd.DataFrame, name: str, values: list, pos: int) -> pd.DataFrame:
    df.insert(pos, name, values, True)
    return df


def get_lyrics_df(mode: str) -> pd.DataFrame:
    global INITIAL_NUMBER_OF_SONGS
    
    NUMBER_OF_SONGS_IN_FOLDER = len(os.listdir('./lyrics_lyricwikia/'))
    if(INITIAL_NUMBER_OF_SONGS > NUMBER_OF_SONGS_IN_FOLDER):
        INITIAL_NUMBER_OF_SONGS = NUMBER_OF_SONGS_IN_FOLDER
    
    lyrics_list = []
    empty_lyrics = []
    data = []
    for i in range(1, INITIAL_NUMBER_OF_SONGS + 1):
        index = "ML" + str(i)
        lyric = open_lyric_from_index(index)
        if(lyric):
            lyric = preprocess(lyric, mode)
        else:
            empty_lyrics.append("ML" + str(i))
        lyrics_list.append(lyric)
        data.append([index, lyric])
    return pd.DataFrame(data, columns=["index", "lyric"]), lyrics_list, empty_lyrics


def extract_total_word_list_from_df(df: pd.DataFrame) -> list:
    return [item for sublist in df['Lyric'].tolist() for item in sublist] 


def create_word_bag(emotion_df: pd.DataFrame) -> Counter:
    word_list = extract_total_word_list_from_df(emotion_df) 
    counter = Counter()
    counter.update(word_list)
    return counter


def cut_bag(bag: Counter, minimum_repetitions: int) -> Counter:
    return Counter(el for el in bag.elements() if bag[el] >= minimum_repetitions)


def get_word_repetitions(counter: Counter):
    word_repetitions = {}
    for word in counter:
        word_repetitions[word] = counter[word]
    return word_repetitions


def get_file_ocurrences(df: pd.DataFrame, counter: Counter): 
    list_of_lyrics = df['Lyric'].tolist()
    ocurrences = {}
    for word in counter:
        n = 0
        for file in list_of_lyrics:
            for w in file:
                if(word == w):
                    n += 1
                    break
        ocurrences[word] = n
    return ocurrences


def calculate_weights(file_ocurrences, word_repetitions):
    weights = {}
    for word in word_repetitions:
        weights[word] = file_ocurrences[word]*word_repetitions[word]/FINAL_NUMBER_OF_SONGS
    return weights
    #for word in counter.most_common():
        #print(word[0], word[1])
 
    
def get_words_data(emotion_df: pd.DataFrame):
    emotion_word_counter = create_word_bag(emotion_df)
    emotion_word_counter = cut_bag(emotion_word_counter, MINIMUM_WORD_REPETITION)

    file_ocurrences = get_file_ocurrences(emotion_df, emotion_word_counter)
    word_repetitions = get_word_repetitions(emotion_word_counter)
    weights = calculate_weights(file_ocurrences, word_repetitions)
    
    # Check for error in word repetitions and file ocurrences
    for word in word_repetitions:
        if(file_ocurrences[word] > word_repetitions[word]):
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!1', word, file_ocurrences[word], word_repetitions[word] )
    
    sorted_data = []
    for key in sorted(word_repetitions.keys()):
        sorted_data.append([key, word_repetitions[key], file_ocurrences[key], weights[key]])
    emotion_words_df = pd.DataFrame(sorted_data, columns=["word", "totalRepetitions", "fileOcurrences", "weight"])
    emotion_words_df = emotion_words_df.sort_values(by='weight', ascending=False)
    return emotion_words_df

def get_bags_data(bigrams_list):
    exit()



def get_all_emotions_bags(df):
    
    DATAFRAME_PATH = "./dataframes/"
    
    if(not os.path.exists(DATAFRAME_PATH)):
        os.makedirs(DATAFRAME_PATH)
    
    relaxed_df = df[df['Emotion'] == 'relaxed']
    RELAXED_SONGS_COUNT = len(relaxed_df.index)
    relaxed_data_df = get_words_data(relaxed_df)
    print('\n\n--------RELAXED--------')
    print("RELAXED SONGS: ", RELAXED_SONGS_COUNT)
    print(relaxed_data_df.head(25))
    
    relaxed_data_df.to_csv(DATAFRAME_PATH + "relaxed_data.csv")

    angry_df = df[df['Emotion'] == 'angry']
    ANGRY_SONGS_COUNT = len(angry_df.index)
    angry_data_df = get_words_data(angry_df)
    print('\n\n--------ANGRY--------')
    print("ANGRY SONGS: ", ANGRY_SONGS_COUNT)
    print(angry_data_df.head(25))
    
    angry_data_df.to_csv(DATAFRAME_PATH + "angry_data.csv")

    happy_df = df[df['Emotion'] == 'happy']
    HAPPY_SONGS_COUNT = len(happy_df.index)
    happy_data_df = get_words_data(happy_df)
    print('\n\n--------HAPPY--------')
    print("HAPPY SONGS: ", HAPPY_SONGS_COUNT)
    print(happy_data_df.head(25))
    
    happy_data_df.to_csv(DATAFRAME_PATH + "happy_data.csv")


    sad_df = df[df['Emotion'] == 'sad']
    SAD_SONGS_COUNT = len(sad_df.index)
    sad_data_df = get_words_data(sad_df)
    print('\n\n--------SAD--------')
    print("SAD SONGS: ", SAD_SONGS_COUNT)
    print(sad_data_df.head(25))
    
    sad_data_df.to_csv(DATAFRAME_PATH + "sad_data.csv")

#TODO
# - Tener en cuenta salto de linea, no deberia ponerse como bigrama la ultima palabra de un verso y la primera del siguiente.
# - Primera palabra en mayuscula?¿?
# - Gestionar bien la tokenizacion. Ahora mismo don't = do + n't | can't = ca + n't. Deberia ser asi? Que hacemos con verbos have, be?
def get_bigrams(df: pd.DataFrame):

    lyrics_list = df['Lyric'].tolist()


    print('------------------------')
    counter = Counter()
    for lyric in lyrics_list:
        bigrams_list = list(bigrams(lyric))
        counter.update(bigrams_list)
        #print(counter)
        #print('------------------------')
    counter = cut_bag(counter, MINIMUM_BIGRAM_REPETITION)
    return counter


def get_all_bigrams(df: pd.DataFrame):

    relaxed_df = df[df['Emotion'] == 'relaxed']
    RELAXED_SONGS_COUNT = len(relaxed_df.index)
    counter = get_bigrams(relaxed_df)
    print('\n\n--------RELAXED--------')
    print("RELAXED SONGS: ", RELAXED_SONGS_COUNT)
    print(counter)

    angry_df = df[df['Emotion'] == 'angry']
    ANGRY_SONGS_COUNT = len(angry_df.index)
    counter = get_bigrams(angry_df)
    print('\n\n--------ANGRY--------')
    print("ANGRY SONGS: ", ANGRY_SONGS_COUNT)
    print(counter)


    happy_df = df[df['Emotion'] == 'happy']
    HAPPY_SONGS_COUNT = len(happy_df.index)
    counter = get_bigrams(happy_df)
    print('\n\n--------HAPPY--------')
    print("HAPPY SONGS: ", HAPPY_SONGS_COUNT)
    print(counter)


    sad_df = df[df['Emotion'] == 'sad']
    SAD_SONGS_COUNT = len(sad_df.index)
    counter = get_bigrams(sad_df)
    print('\n\n--------SAD--------')
    print("SAD SONGS: ", SAD_SONGS_COUNT)
    print(counter)


def main():
    global FINAL_NUMBER_OF_SONGS
    global INITIAL_NUMBER_OF_SONGS
    
    if(INITIAL_NUMBER_OF_SONGS <= 0):
        INITIAL_NUMBER_OF_SONGS = 1000000
    # ----------------------------------
    # ------------ word bags -----------
    # ----------------------------------
    
    df = read_csv_as_df(LYRICS_DATASET_PATH)
    lyrics_df,  lyrics_list, empty_lyrics = get_lyrics_df(UNIGRAMS_MODE)
    df_with_lyrics = insert_column_to_df(df, "Lyric", lyrics_list, 3)
    FINAL_NUMBER_OF_SONGS = INITIAL_NUMBER_OF_SONGS - len(empty_lyrics)
    
    print('empty_lyrics: ', empty_lyrics)
    print(df_with_lyrics)
    print("TOTAL SONGS: ", len(df_with_lyrics.index))

    get_all_emotions_bags(df_with_lyrics)
    exit()
    # ----------------------------------
    # ----------------------------------
    # ----------------------------------




    # ----------------------------------
    # ------------- bigrams ------------
    # ----------------------------------
    
    df = read_csv_as_df(LYRICS_DATASET_PATH)
    df_with_lyrics, empty_lyrics = insert_lyrics_to_df(df, BIGRAMS_MODE)
    FINAL_NUMBER_OF_SONGS = INITIAL_NUMBER_OF_SONGS - len(empty_lyrics)
    
    get_all_bigrams(df)

    # ----------------------------------
    # ----------------------------------
    # ----------------------------------
    





if __name__ == "__main__":
    main()