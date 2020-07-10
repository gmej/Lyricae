from nltk.util import bigrams
import pandas as pd
import os
import string
from analysis_scraping_data.functions.lyrics_functions import *
from progress.bar import Bar # progress bar


#NUMBER_OF_SONGS = len(os.listdir('./lyrics_lyricwikia/'))
INITIAL_NUMBER_OF_SONGS = -1
MINIMUM_WORD_REPETITION = 50
MINIMUM_BIGRAM_REPETITION = 4
FINAL_NUMBER_OF_SONGS = INITIAL_NUMBER_OF_SONGS

DATAFRAME_PATH = "../dataframes/"
LYRICS_DATASET_PATH = '../lyrics_dataset/MoodyLyrics.csv'

def read_csv_as_df(path: str) -> pd.DataFrame:    
    csv_df = pd.read_csv(path, na_values=['.'], dtype={'Index': str, 'Artist': str, 'Song': str, 'Emotion': str})
    return csv_df.head(INITIAL_NUMBER_OF_SONGS)


def insert_column_to_df(df: pd.DataFrame, name: str, values: list, pos: int) -> pd.DataFrame:
    df.insert(pos, name, values, True)
    return df


def get_lyrics_df(mode: int = 1) -> pd.DataFrame:
    global INITIAL_NUMBER_OF_SONGS
    
    NUMBER_OF_SONGS_IN_FOLDER = len(os.listdir('../lyrics_lyricwikia/'))
    if(INITIAL_NUMBER_OF_SONGS > NUMBER_OF_SONGS_IN_FOLDER):
        INITIAL_NUMBER_OF_SONGS = NUMBER_OF_SONGS_IN_FOLDER
    print('INITIAL_NUMBER_OF_SONGS: ', INITIAL_NUMBER_OF_SONGS)
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

def create_bigram_bag(lyrics_list: list) -> Counter:
    counter = Counter()
    bigrams_set = set()
    for lyric in lyrics_list:
        bigrams_list = list(bigrams(lyric))
        bigrams_set = bigrams_set.union(set(bigrams_list))
        counter.update(bigrams_list)
    return counter, bigrams_set


def cut_bag(bag: Counter, minimum_repetitions: int) -> Counter:
    return Counter(el for el in bag.elements() if bag[el] >= minimum_repetitions)

def cut_bigram_bag(bag: Counter, set: set, minimum_repetitions: int) -> Counter:
    bigram_list = []
    counter = Counter()
    for bi in set:
        if(bag[bi] >= minimum_repetitions):
            counter.update({bi: bag[bi]})
    return counter

def get_gram_repetitions(counter: Counter) -> dict:
    word_repetitions = {}
    for word in counter:
        word_repetitions[word] = counter[word]
    return word_repetitions


def get_file_ocurrences(df: pd.DataFrame, counter: Counter) -> dict: 
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

def get_bigram_file_ocurrences(lyrics_list: list, counter: Counter, bigram_set: set) -> dict:
    bar = Bar('calculating bigrams file ocurrences', max = len(bigram_set))
    ocurrences = {}
    for bigram in bigram_set:
        n = 0
        for file in lyrics_list:
            file_bigrams = bigrams(file)
            for bi in file_bigrams:
                if(bigram == bi):
                    n+=1
                    break
        ocurrences[bigram] = n
        bar.next()
    return ocurrences        

def calculate_weights(file_ocurrences: dict, gram_repetitions: dict) -> dict:
    weights = {}
    for gram in gram_repetitions:
        weights[gram] = file_ocurrences[gram]*gram_repetitions[gram]/FINAL_NUMBER_OF_SONGS
    return weights


def get_words_complete_data(emotion_df: pd.DataFrame) -> pd.DataFrame:
    emotion_word_counter = create_word_bag(emotion_df)
    emotion_word_counter = cut_bag(emotion_word_counter, MINIMUM_WORD_REPETITION)

    file_ocurrences = get_file_ocurrences(emotion_df, emotion_word_counter)
    word_repetitions = get_gram_repetitions(emotion_word_counter)
    weights = calculate_weights(file_ocurrences, word_repetitions)
    
    # Checks for error in word repetitions and file ocurrences
    for word in word_repetitions:
        if(file_ocurrences[word] > word_repetitions[word]):
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!1', word, file_ocurrences[word], word_repetitions[word] )
    
    sorted_data = []
    for key in sorted(word_repetitions.keys()):
        sorted_data.append([key, word_repetitions[key], file_ocurrences[key], weights[key]])
    emotion_words_df = pd.DataFrame(sorted_data, columns=["word", "totalRepetitions", "fileOcurrences", "weight"])
    emotion_words_df = emotion_words_df.sort_values(by='weight', ascending=False)
    return emotion_words_df



def get_all_emotions_bags(df: pd.DataFrame):
    
    
    if(not os.path.exists(DATAFRAME_PATH)):
        os.makedirs(DATAFRAME_PATH)
    

    relaxed_df = df[df['Emotion'] == 'relaxed']
    RELAXED_SONGS_COUNT = len(relaxed_df.index)
    relaxed_unigram_data = get_words_complete_data(relaxed_df)
    print('\n\n--------RELAXED--------')
    print("RELAXED SONGS: ", RELAXED_SONGS_COUNT)
    print(relaxed_unigram_data.head(25))
    print('\n\n--------RELAXED--------')
    print(relaxed_unigram_data.sort_values(by="totalRepetitions", ascending=False).head(25))
    print('\n\n--------RELAXED--------')
    print(relaxed_unigram_data.sort_values(by="fileOcurrences", ascending=False).head(25))
    relaxed_unigram_data.to_csv(DATAFRAME_PATH + "relaxed_unigram_data.csv")


    angry_df = df[df['Emotion'] == 'angry']
    ANGRY_SONGS_COUNT = len(angry_df.index)
    angry_unigram_data = get_words_complete_data(angry_df)
    print('\n\n--------ANGRY--------')
    print("ANGRY SONGS: ", ANGRY_SONGS_COUNT)
    print(angry_unigram_data.head(25))
    
    angry_unigram_data.to_csv(DATAFRAME_PATH + "angry_unigram_data.csv")

    happy_df = df[df['Emotion'] == 'happy']
    HAPPY_SONGS_COUNT = len(happy_df.index)
    happy_unigram_data = get_words_complete_data(happy_df)
    print('\n\n--------HAPPY--------')
    print("HAPPY SONGS: ", HAPPY_SONGS_COUNT)
    print(happy_unigram_data.head(25))
    print('\n\n--------HAPPY--------')
    print(happy_unigram_data.sort_values(by="totalRepetitions", ascending=False).head(25))
    print('\n\n--------HAPPY--------')
    print(happy_unigram_data.sort_values(by="fileOcurrences", ascending=False).head(25))
    
    happy_unigram_data.to_csv(DATAFRAME_PATH + "happy_unigram_data.csv")


    sad_df = df[df['Emotion'] == 'sad']
    SAD_SONGS_COUNT = len(sad_df.index)
    sad_unigram_data = get_words_complete_data(sad_df)
    print('\n\n--------SAD--------')
    print("SAD SONGS: ", SAD_SONGS_COUNT)
    print(sad_unigram_data.head(25))
    
    sad_unigram_data.to_csv(DATAFRAME_PATH + "sad_unigram_data.csv")
    
    
    '''  
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(relaxed_data_df)
        print(angry_data_df)
        print(happy_data_df)
        print(sad_data_df)
    '''

def get_bigrams_complete_data(emotion_df: pd.DataFrame):
    list_of_lyrics = emotion_df['Lyric'].tolist()
    
    emotion_bigram_bag, bigram_set = create_bigram_bag(list_of_lyrics) 
    emotion_bigram_bag = cut_bigram_bag(emotion_bigram_bag, bigram_set, MINIMUM_BIGRAM_REPETITION)

    bigram_file_ocurrences = get_bigram_file_ocurrences(list_of_lyrics, emotion_bigram_bag, bigram_set)
    bigrams_repetitions = get_gram_repetitions(emotion_bigram_bag)
    weights = calculate_weights(bigram_file_ocurrences, bigrams_repetitions)
    sorted_bigrams_repetitions = {k: v for k, v in sorted(bigrams_repetitions.items(), key=lambda item: item[1])}
    #print(sorted_bigrams_repetitions)
    #sorted_ocurrences = {k: v for k, v in sorted(bigram_file_ocurrences.items(), key=lambda item: item[1])}
    #print(sorted_ocurrences) 
    
    sorted_data = []
    for bigram in sorted(bigrams_repetitions.keys()):
        sorted_data.append([bigram, bigram[0], bigram[1], bigrams_repetitions[bigram], bigram_file_ocurrences[bigram], weights[bigram]])
    emotion_bigrams_df = pd.DataFrame(sorted_data, columns=["bigram", "word1", "word2", "totalRepetitions", "fileOcurrences", "weight"])
    emotion_bigrams_df = emotion_bigrams_df.sort_values(by='weight', ascending=False)

    return emotion_bigrams_df

   


def get_all_emotion_bigrams(df: pd.DataFrame):

    relaxed_df = df[df['Emotion'] == 'relaxed']
    RELAXED_SONGS_COUNT = len(relaxed_df.index)
    relaxed_bigram_data = get_bigrams_complete_data(relaxed_df)
    print('\n\n--------RELAXED--------')
    print("RELAXED SONGS: ", RELAXED_SONGS_COUNT)
    print(relaxed_bigram_data.head(25))
    
    relaxed_bigram_data.to_csv(DATAFRAME_PATH + "relaxed_bigram_data.csv")


    angry_df = df[df['Emotion'] == 'angry']
    ANGRY_SONGS_COUNT = len(angry_df.index)
    angry_bigram_data = get_bigrams_complete_data(angry_df)
    print('\n\n--------ANGRY--------')
    print("ANGRY SONGS: ", ANGRY_SONGS_COUNT)
    print(angry_bigram_data.head(25))
    
    angry_bigram_data.to_csv(DATAFRAME_PATH + "angry_bigram_data.csv")


    happy_df = df[df['Emotion'] == 'happy']
    HAPPY_SONGS_COUNT = len(happy_df.index)
    happy_bigram_data = get_bigrams_complete_data(happy_df)
    print('\n\n--------HAPPY--------')
    print("HAPPY SONGS: ", HAPPY_SONGS_COUNT)
    print(happy_bigram_data.head(25))
    
    happy_bigram_data.to_csv(DATAFRAME_PATH + "happy_bigram_data.csv")


    sad_df = df[df['Emotion'] == 'sad']
    SAD_SONGS_COUNT = len(sad_df.index)
    sad_bigram_data = get_bigrams_complete_data(sad_df)
    print('\n\n--------SAD--------')
    print("SAD SONGS: ", SAD_SONGS_COUNT)
    print(sad_bigram_data.head(25))
    
    sad_bigram_data.to_csv(DATAFRAME_PATH + "sad_bigram_data.csv")



def main():
    global FINAL_NUMBER_OF_SONGS
    global INITIAL_NUMBER_OF_SONGS
    
    if(INITIAL_NUMBER_OF_SONGS <= 0):
        INITIAL_NUMBER_OF_SONGS = 1000000
    
    
    
    df = read_csv_as_df(LYRICS_DATASET_PATH)

    lyrics_df,  lyrics_list, empty_lyrics = get_lyrics_df()
    df_with_lyrics = insert_column_to_df(df, "Lyric", lyrics_list, 4)

    FINAL_NUMBER_OF_SONGS = INITIAL_NUMBER_OF_SONGS - len(empty_lyrics)
    
    print('empty_lyrics: ', empty_lyrics)
    print(df_with_lyrics)
    print("TOTAL SONGS: ", len(df_with_lyrics.index))
     
    
    df_with_lyrics.to_csv(DATAFRAME_PATH + "initial_dataframe.csv")

    # ----------------------------------
    # ------------ word bags -----------
    # ----------------------------------
    

    get_all_emotions_bags(df_with_lyrics)
    
    
    # ----------------------------------
    # ----------------------------------
    # ----------------------------------



    # ----------------------------------
    # ------------- bigrams ------------
    # ----------------------------------
    
    df = read_csv_as_df(LYRICS_DATASET_PATH)
    lyrics_df,  lyrics_list, empty_lyrics = get_lyrics_df(mode=2)
    df_with_lyrics = insert_column_to_df(df, "Lyric", lyrics_list, pos=3)
    print(df_with_lyrics)


    #get_all_emotion_bigrams(df_with_lyrics)

    # ----------------------------------
    # ----------------------------------
    # ----------------------------------
    



if __name__ == "__main__":
    main()