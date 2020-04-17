from nltk.util import bigrams
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import pandas as pd
import numpy as np
import types

DATAFRAME_PATH = "./dataframes/"

SENTIMENTS = {
    1: "happy",
    2: "angry",
    3: "relaxed",
    4: "sad",
}

#MOCK
selected_sentiment = 3
user_input = 'I feel'




def preprocess(lyric: str) -> list:
    lyric = lyric.lower()
    
    lyric = lyric.replace("can't", 'can not')
    lyric = lyric.replace("won't", 'will not')
    lyric = lyric.replace("'d", ' would')
    lyric = lyric.replace("gonna", 'going to')
    lyric = lyric.replace("wanna", 'want to')
    lyric = lyric.replace("gotta", 'got to')
    lyric = lyric.replace("'cause", 'because')
    lyric = lyric.replace("'bout", 'about')
    
    #tokenize
    remove_list = ["'s", "n't", "'m", "'re", "'ll", "'ve", "'d", "'ll"]
    word_list = word_tokenize(lyric)
    words = [x for x in word_list if x not in remove_list]
    
    
    #remove punctuation  
    punctuation = set(string.punctuation)
    custom_punctuation = set(["...", "''", "'", "`", "``"])
    punctuation = punctuation.union(custom_punctuation)
    return [w for w in words if  w not in punctuation]

def preprocess_unigram(words: list) -> list:
    
    #remove stopwords
    stoplist = stopwords.words('english')
    words = [w for w in words if w not in stoplist]
    return words


def process_input(user_input: str) -> list:
    preprocessed = preprocess(user_input)
    unigrams_list = preprocess_unigram(preprocessed)
    bigrams_list = list(bigrams(preprocessed))

    
    return unigrams_list, bigrams_list


def load_data(sentiment: str) -> pd.DataFrame:
    unigram_df = pd.read_csv(DATAFRAME_PATH + sentiment + "_unigram_data.csv",
                              dtype={'word': str, 'totalRepetitions': int, 'fileOcurrences': int, 'weight': float})
    bigram_df = pd.read_csv(DATAFRAME_PATH + sentiment + "_bigram_data.csv")
    similarities_df = pd.read_csv(DATAFRAME_PATH + sentiment + "_similarities.csv", index_col= 'word')
    
    return unigram_df, bigram_df, similarities_df

#RECOMMENDATION
def recommend_most_common_words(unigram_df: pd.DataFrame, number: int) -> list:

    words = unigram_df.nlargest(number, 'weight')
    return words['word'].tolist()

#RECOMMENDATION
#TODO ¿tener en cuenta el peso?
def recommend_keyed_vectors(unigrams: list, similarities: pd.DataFrame, number: int = 5):
    recommendations = {}
    for word in unigrams:
        if word in similarities:
            column_series = similarities[word]
            most_similar = column_series.sort_values(ascending=False).nlargest(number)
            most_similar_words = most_similar.index.values.tolist()
            recommendations[word] = most_similar_words
    return recommendations


#RECOMMENDATION
def recommend_most_common_ngrams(ngram_df: pd.DataFrame, number: int) -> list:
    ngrams = ngram_df.nlargest(number, 'weight')
    return ngrams['word'].tolist()

def dict_iter_V2(dictionary: dict, deep: int = 3, bigram_df: pd.DataFrame = None):
    deep -= 1
    if(deep == 0):
        return dictionary
    for el in dictionary:
        new_items = next_words_list(el, bigram_df)
        new_d = {}
        if(deep > 1):
            for item in new_items:
                new_d[item] = None  # espacio para el nuevo dict
            dictionary[el] = dict_iter_V2(new_d, deep, bigram_df)
        else:
            dictionary[el] = new_items
    return dictionary
    


def next_bigrams(word, bigram_df):
    next_df = bigram_df.loc[bigram_df['word1'] == word]
    next_words = next_df.head(3)['word2'].tolist()
    next_words_dict = dict.fromkeys(next_words, {})
    return next_words_dict

def next_words_list(word, bigram_df):
    next_df = bigram_df.loc[bigram_df['word1'] == word]
    next_words = next_df.head(3)['word2'].tolist()
    next_words_dict = dict.fromkeys(next_words, {})
    return next_words

def recommend_bigrams(bigrams_input: list, bigram_df: pd.DataFrame):
    NUMBER_OF_ITERATIONS = 3
    print(bigram_df.head(20))
    
    #for bigram in bigrams_input:
        #print(bigram[0], ' ', bigram[1])
        #bigram_df.loc[bigram_df['bigram'] == bigram_str]
        #print(bigram_df.loc(bigram_str))
    
    #print(bigrams_input)
    print("\n\n\n")
    print('INPUT: ', bigrams_input[len(bigrams_input)-1][0], bigrams_input[len(bigrams_input)-1][1])
    print("\n")
    
    last_word = bigrams_input[len(bigrams_input)-1][1]
    next_words_dict = next_bigrams(last_word, bigram_df)
    final_dict = dict_iter_V2(next_words_dict, 3, bigram_df)
    pretty_dict(final_dict)
    '''
    i = 0
    for word in next_words:
        next_df = bigram_df.loc[bigram_df['word1'] == word]
        next_list = next_df.head(3)['word2'].tolist()
        j=0
        for item in next_list:
            #next_words[i][j] = item
            next_words_dict[word][item] = {}
            j +=1
        i +=1
    print(next_words_dict)
    
    print(next_words)
    '''
        

def pretty_dict(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty_dict(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))


#RECOMMENDATION
def recommend_next_bigram(word: str) -> tuple:
    return

def main():
    sentiment = SENTIMENTS[selected_sentiment]
    unigrams_input, bigrams_input = process_input(user_input)
    print('input_unigrams: ', unigrams_input)
    print('input_bigrams: ', bigrams_input)
    
    unigram_df, bigram_df, similarities_df = load_data(sentiment)

    print('RECOMMENDATIONS FOR USER INPUT: ', user_input)
    recommend_bigrams(bigrams_input, bigram_df)
    #most_common_words = recommend_most_common_words(unigram_df, 10)
    
    #most_similar_words = recommend_keyed_vectors(unigrams, similarities_df, 6)
    
    #most_common_bigrams = recommend_most_common_ngrams(bigram_df, 8)
    
    




if __name__ == "__main__":
    main()