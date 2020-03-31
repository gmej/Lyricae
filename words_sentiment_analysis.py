from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd
import numpy as np
import re #Regular expression operations
import os
import time, string

#NUMBER_OF_SONGS = len(os.listdir('./lyrics_lyricwikia/'))
INITIAL_NUMBER_OF_SONGS = 5000
MINIMUM_WORD_REPETITION = 50

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


def get_df_from_lyrics_csv():    
    csv_df = pd.read_csv('./datasets/MoodyLyrics.csv', 
                         na_values=['.'])
    return csv_df.head(INITIAL_NUMBER_OF_SONGS)


def insert_lyrics_to_df(df: pd.DataFrame):
    global INITIAL_NUMBER_OF_SONGS
    
    df.index += 1 # Start index = 1
    lyrics = []
    empty_lyrics = []
    
    if(INITIAL_NUMBER_OF_SONGS > len(df.index)):
        INITIAL_NUMBER_OF_SONGS = len(df.index)
    
    for i in range(1, INITIAL_NUMBER_OF_SONGS + 1):
        lyric = get_lyric("ML" + str(i))
        if(lyric):
            lyric = preprocess(lyric)
        else:
            empty_lyrics.append("ML" + str(i))
        lyrics.append(lyric)
    
    df.insert(3, "Lyric", lyrics, True)
    
    return df, empty_lyrics


def word_bags(emotion_df: pd.DataFrame):
    
    #print(emotion_df.loc[emotion_df['Index'] == 'ML417'])
    #print(emotion_df[416:419])
    #print(emotion_df.loc[[412, 417, 420, 423], :])
    word_list = [item for sublist in emotion_df['Lyric'].tolist() for item in sublist] 
    counter = Counter()
    counter.update(word_list)
    counter = cut_bag(counter, MINIMUM_WORD_REPETITION)
    return counter


def cut_bag(bag: Counter, minimum_repetitions: int):
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
                    break;
        ocurrences[word] = n
    return ocurrences


def get_weights(file_ocurrences, word_repetitions):
    weights = {}
    for word in word_repetitions:
        weights[word] = file_ocurrences[word]*word_repetitions[word]/FINAL_NUMBER_OF_SONGS
    return weights
    #for word in counter.most_common():
        #print(word[0], word[1])
    
def get_emotion_data(emotion_df: pd.DataFrame):
    emotion_word_counter = word_bags(emotion_df)

    file_ocurrences = get_file_ocurrences(emotion_df, emotion_word_counter)
    word_repetitions = get_word_repetitions(emotion_word_counter)
    weights = get_weights(file_ocurrences, word_repetitions)
    
    # Check for error in word repetitions and file ocurrences
    for word in word_repetitions:
        if(file_ocurrences[word] > word_repetitions[word]):
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!1', word, file_ocurrences[word], word_repetitions[word] )
    
    sorted_data = []
    for key in sorted(word_repetitions.keys()):
        sorted_data.append([key, word_repetitions[key], file_ocurrences[key], weights[key]])
    #emotion_words_df = pd.DataFrame(columns= ["Word", "TotalRepetitions", "FileOcurrences", "Weight"])
    #emotion_words_df = pd.DataFrame(index= word_repetitions.keys(), "TotalRepetitions" = word_repetitions.values(), "FileOcurrences" = file_ocurrences.values(), "Weight" = weights.values())
    emotion_words_df = pd.DataFrame(sorted_data, columns=["word", "totalRepetitions", "fileOcurrences", "weight"])
    emotion_words_df = emotion_words_df.sort_values(by='weight', ascending=False)
    return emotion_words_df
    
df = get_df_from_lyrics_csv()
df, empty_lyrics = insert_lyrics_to_df(df)
FINAL_NUMBER_OF_SONGS = INITIAL_NUMBER_OF_SONGS - len(empty_lyrics)
print(df)

print('empty_lyrics: ', empty_lyrics)
#print(df[415:418])
print("TOTAL SONGS: ", len(df.index))



relaxed_df = df[df['Emotion'] == 'relaxed']
RELAXED_SONGS_COUNT = len(relaxed_df.index)
relaxed_data_df = get_emotion_data(relaxed_df)
print('\n\n--------RELAXED--------')
print("RELAXED SONGS: ", RELAXED_SONGS_COUNT)
print(relaxed_data_df.head(25))

relaxed_df = df[df['Emotion'] == 'angry']
ANGRY_SONGS_COUNT = len(relaxed_df.index)
relaxed_data_df = get_emotion_data(relaxed_df)
print('\n\n--------ANGRY--------')
print("ANGRY SONGS: ", ANGRY_SONGS_COUNT)
print(relaxed_data_df.head(25))


relaxed_df = df[df['Emotion'] == 'happy']
HAPPY_SONGS_COUNT = len(relaxed_df.index)
relaxed_data_df = get_emotion_data(relaxed_df)
print('\n\n--------HAPPY--------')
print("HAPPY SONGS: ", HAPPY_SONGS_COUNT)
print(relaxed_data_df.head(25))


relaxed_df = df[df['Emotion'] == 'sad']
SAD_SONGS_COUNT = len(relaxed_df.index)
relaxed_data_df = get_emotion_data(relaxed_df)
print('\n\n--------SAD--------')
print("SAD SONGS: ", SAD_SONGS_COUNT)
print(relaxed_data_df.head(25))



