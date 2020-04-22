from nltk.util import bigrams
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import pandas as pd

#from sentiments import SENTIMENTS

DATAFRAME_PATH = "../../dataframes/"




#MOCK
#selected_sentiment = 3
#user_input = 'I feel'
#user_input = 'I feel like my soul is'




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


def create_dict_recursively(dictionary: dict, depth: int = 3, bigram_df: pd.DataFrame = None):
    depth -= 1
    if(depth == 0):
        return dictionary
    for el in dictionary:
        new_items = next_words_list(el, bigram_df)
        new_d = {}
        if(depth > 1):
            for item in new_items:
                new_d[item] = None  # espacio para el nuevo dict
            dictionary[el] = create_dict_recursively(new_d, depth, bigram_df)
        else:
            dictionary[el] = new_items
    return dictionary


#RECOMMENDATION
def recommend_most_common_words(unigram_df: pd.DataFrame, number: int) -> list:
    words = unigram_df.nlargest(number, 'weight')
    return words['word'].tolist()

#RECOMMENDATION
def recommend_most_common_ngrams(ngram_df: pd.DataFrame, number: int) -> list:
    ngram_df = ngram_df.head(number)
    ngrams = ngram_df.nlargest(number, 'weight')
    word1 = ngram_df['word1'].tolist()
    word2 = ngram_df['word2'].tolist()
    lista = []
    for i in range(0, len(word1)):
        lista.append((word1[i] + ' ' + word2[i]))
    return lista


#RECOMMENDATION
#TODO ¿tener en cuenta el peso?
#TODO Recomienda la propia palabra
def recommend_keyed_vectors(unigrams: list, similarities: pd.DataFrame, number: int = 5):
    recommendations = {}
    for word in unigrams:
        if word in similarities:
            column_series = similarities[word]
            most_similar = column_series.sort_values(ascending=False).nlargest(number)
            most_similar_words = most_similar.index.values.tolist()
            if(most_similar_words[0] == word):
                most_similar_words.pop(0)
            recommendations[word] = most_similar_words
    print(recommendations)
    return recommendations




def next_words_dict(word, bigram_df):
    next_df = bigram_df.loc[bigram_df['word1'] == word]
    next_words = next_df.head(3)['word2'].tolist()
    next_words_dict = {}
    for el in next_words:
        next_words_dict[el] = None
    return next_words_dict

def next_words_list(word, bigram_df):
    next_df = bigram_df.loc[bigram_df['word1'] == word]
    next_words = next_df.head(3)['word2'].tolist()
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


def recommend_bigrams(bigrams_input: list, bigram_df: pd.DataFrame, depth:int):

    #RECOMMENDATION BASED ON LAST WORD
    last_word = bigrams_input[len(bigrams_input)-1][1]
    next_words = next_words_dict(last_word, bigram_df)
    final_dict = create_dict_recursively(next_words, depth, bigram_df)
    recommendations = []
    d = flatten_dict(final_dict)
    strings = convert_dict_to_list(d)
    #print(result)
    #pretty_dict(final_dict)
    return strings


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

def sentiment_selection(sentiment: str, n_words: int, n_bigrams: int) -> dict:
    unigram_df = load_unigrams_data(sentiment)
    bigram_df = load_bigrams_data(sentiment)
    
    most_common_words = recommend_most_common_words(unigram_df, n_words)
    most_common_bigrams = recommend_most_common_ngrams(bigram_df, n_bigrams)
    
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
        return {
        'most_similar_words': most_similar_words,
        }
    else:
        next_bigrams = recommend_bigrams(bigrams_input, bigram_df, n_next_bigrams)
        return {
            'most_similar_words': most_similar_words,
            'next_bigrams': next_bigrams}
    

