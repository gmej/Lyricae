#
# first time, we have to do this:
#
#import nltk
#nltk.download() # install corpus 'book'
#
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords

import time, string

def open_lyric(file_path):
    with open(file_path) as f:
        return f.read()

def get_sentences(lyric):
    return sent_tokenize(lyric)

def get_words(lyric):
    return word_tokenize(lyric)

def stem(lyric, stemmer='porter'):
    words = "boys children are have is has Madrid"
    
    if(stemmer == 'porter'):
        start = time.time()
        porter = PorterStemmer()
        print("Porter: " + " ".join([porter.stem(w) for w in word_tokenize(words)]))
    elif(stemmer == 'lancaster'):
        start = time.time()
        lancaster = LancasterStemmer()
        print("Lancaster: " + " ".join([lancaster.stem(w) for w in word_tokenize(words)]))
    elif(stemmer == 'wordnet'):
        start = time.time()
        wordnet = WordNetLemmatizer()
        print("WordNet: " + " ".join([wordnet.lemmatize(w) for w in word_tokenize(words)]))
    elif(stemmer == 'english'):
        start = time.time()
        snowball = EnglishStemmer()
        print("SnowBall: " + " ".join([snowball.stem(w) for w in word_tokenize(words)]))
    
    end = time.time()
    print("Execution time: "  + str(end - start))

def lemmatize(words):
    wordnet = WordNetLemmatizer()
    lemmas = [wordnet.lemmatize(word, pos='v') for word in words] # 'j' adj | 'n' noun | 'v' verb | ' r' adv
    #print("WordNet lemmatization: " + lemmas.__str__())
    return lemmas

def remove_stopwords(words):
    stoplist = stopwords.words('english')
    #print(stoplist)
    return [w for w in words if w not in stoplist]

def remove_punctuation(words):
    punctuation = set(string.punctuation)
    print(punctuation)
    return [w for w in words if  w not in punctuation]


def preprocess(lyric):
    lyric = lyric.lower()
    lyric = lyric.replace("\n", ' ')
    lyric = lyric.replace("\r", ' ')
    lyric = lyric.replace("\r\n", ' ')
    words = get_words(lyric)
    lemmas = lemmatize(words)
    lemmas = remove_stopwords(lemmas) # i, you, me...
    print(lemmas)
    clean_lemmas = remove_punctuation(lemmas) # i, you, me...
    print(clean_lemmas)
    #before this i should use punctuation for something
    
    
    
lyric = open_lyric('./lyrics_lyricwikia/angry_Marilyn.Manson_Sweet.Dreams.')
preprocess(lyric)