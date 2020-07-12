from nltk.util import bigrams
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import pandas as pd
import random
#from sentiments import SENTIMENTS

DATAFRAME_PATH = "../../dataset/dataframes/"

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


def load_unigrams_data(sentiment: str) -> pd.DataFrame:
    unigram_df = pd.read_csv(DATAFRAME_PATH + sentiment + "_unigram_data.csv",
        dtype={'word': str, 'totalRepetitions': int, 'fileOcurrences': int, 'weight': float})
    return unigram_df


def load_bigrams_data(sentiment: str) -> pd.DataFrame:
    bigram_df = pd.read_csv(DATAFRAME_PATH + sentiment + "_bigram_data.csv")
    return bigram_df


def load_similarities(sentiment: str) -> pd.DataFrame:
    similarities_df = pd.read_csv(DATAFRAME_PATH + sentiment + "_similarities.csv", index_col= 'word')
    return similarities_df


def create_dict_recursively(dictionary: dict,number: int = 4, depth: int = 2, bigram_df: pd.DataFrame = None):
    depth -= 1
    if(depth == 0):
        return dictionary
    for el in dictionary:
        new_items = next_words_list(el, bigram_df, number)
        new_d = {}
        if(depth > 1):
            for item in new_items:
                new_d[item] = None  # espacio para el nuevo dict
            dictionary[el] = create_dict_recursively(new_d, number, depth, bigram_df)
        else:
            dictionary[el] = new_items
    return dictionary


def shuffle_dict(dictionary: dict):
    keys = list(dictionary.keys())
    random.shuffle(keys)
    shuffle_dict = {}
    for key in keys:
        if(isinstance(dictionary[key], list)):
            lista = dictionary[key]
            random.shuffle(lista)
            shuffle_dict[key] = lista
        else:
            shuffle_dict[key] = dictionary[key]
    return shuffle_dict
    

def next_words_dict(word, bigram_df, number):
    next_df = bigram_df.loc[bigram_df['word1'] == word]
    next_words = next_df.head(number)['word2'].tolist()
    next_words_dict = {}
    for el in next_words:
        next_words_dict[el] = None
    return next_words_dict


def next_words_list(word, bigram_df, number):
    next_df = bigram_df.loc[bigram_df['word1'] == word]
    next_words = next_df.head(number)['word2'].tolist()
    return next_words


def flatten_dict(d, parent_key='', sep=' '):
    import collections
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def convert_dict_to_list(d):
    strings = []
    for k in d:
        for el in d[k]:
            strings.append(k + ' ' + el)
    return strings

def convert_values_to_new_range(values: list, new_min: float = 15, new_max: float = 40):
    old_min = min(values)
    old_max = max(values)
    old_range = (old_max - old_min)  
    new_range = (new_max - new_min)  
    new_list = []
    i =0
    for el in values:
        new_value = (((el - old_min) * new_range) / old_range) + new_min
        new_list.append(new_value)
        i+=1
    return new_list

#RECOMMENDATION
def recommend_most_common_words(unigram_df: pd.DataFrame) -> list:
    N_UNIGRAM_RECOMMENDATIONS = 30
    words_df = unigram_df.nlargest(N_UNIGRAM_RECOMMENDATIONS, 'weight')
    words_list = words_df['word'].tolist()
    weights_list = words_df['weight'].tolist()
    converted_weights = convert_values_to_new_range(weights_list)
    mostCommonUnigrams = []
    for i in range(0,len(words_list)-1):
        mostCommonUnigrams.append({
            "value": words_list[i],
            "count": converted_weights[i],
        })
    return mostCommonUnigrams


#RECOMMENDATION
def recommend_most_common_ngrams(ngram_df: pd.DataFrame) -> list:
    N_NGRAM_RECOMMENDATIONS = 50
    ngram_df = ngram_df.nlargest(N_NGRAM_RECOMMENDATIONS, 'weight')
    word1_list = ngram_df['word1'].tolist()
    word2_list = ngram_df['word2'].tolist()
    weights_list = ngram_df['weight'].tolist()
    converted_weights = convert_values_to_new_range(weights_list)
    mostCommonNGrams = []
    for i in range(0, len(word1_list)-1):
        ngram = (word1_list[i] + ' ' + word2_list[i])
        mostCommonNGrams.append({
            "value": ngram,
            "count": converted_weights[i],
        })    
    return mostCommonNGrams


#RECOMMENDATION
def recommend_keyed_vectors(unigrams: list, similarities: pd.DataFrame, number: int = 5):
    if(len(unigrams) <1):
        return
    recommendations = {}
    for word in unigrams:
        if word in similarities:
            column_series = similarities[word]
            most_similar = column_series.sort_values(ascending=False).nlargest(number+1)
            most_similar_words = most_similar.index.values.tolist()
            if(most_similar_words[0] == word):
                most_similar_words.pop(0)
            recommendations[word] = most_similar_words
    shuffled_recommendations = shuffle_dict(recommendations)
    return shuffled_recommendations


# RECOMMENDATION
#RECOMMENDATION BASED ON LAST WORD
def recommend_bigrams(bigrams_input: list, bigram_df: pd.DataFrame, number:int):
    if(len(bigrams_input) <1):
        return

    last_word = bigrams_input[len(bigrams_input)-1][1]
    next_words = next_words_dict(last_word, bigram_df, number)
    recommendations_dict = create_dict_recursively(next_words, number, 3, bigram_df)
    flat_dict = flatten_dict(recommendations_dict)
    strings = convert_dict_to_list(flat_dict)
    return strings


def pretty_dict(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty_dict(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))


def sentiment_selection(sentiment: str) -> dict:
    unigram_df = load_unigrams_data(sentiment)
    bigram_df = load_bigrams_data(sentiment)
    
    most_common_words = recommend_most_common_words(unigram_df)
    most_common_bigrams = recommend_most_common_ngrams(bigram_df)
    
    return {
        'most_common_words': most_common_words,
        'most_common_bigrams': most_common_bigrams
    }

def get_recommendations(sentiment: str, user_input: str, n_similar_words: int, n_next_bigrams: int):
    n_words = user_input.split()
    
    unigrams_input, bigrams_input = process_input(user_input)
    
    unigram_df = load_unigrams_data(sentiment)
    bigram_df = load_bigrams_data(sentiment)
    similarities_df = load_similarities(sentiment)

    most_similar_words = recommend_keyed_vectors(unigrams_input, similarities_df, n_similar_words)

    if(len(n_words) < 2):
        next_bigrams = recommend_bigrams(unigrams_input, bigram_df, n_next_bigrams)
        
        return {
        'most_similar_words': most_similar_words,
            'next_bigrams': next_bigrams
        }
    else:
        next_bigrams = recommend_bigrams(bigrams_input, bigram_df, n_next_bigrams)
        return {
            'most_similar_words': most_similar_words,
            'next_bigrams': next_bigrams}
    

