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
from nltk import pos_tag, word_tokenize
from nltk.chunk.regexp import *
from nltk import pos_tag, word_tokenize


import nltk

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

# def lemmatize(words):
#     wordnet = WordNetLemmatizer()
#     lemmas = [wordnet.lemmatize(word, pos='v') for word in words] # 'j' adj | 'n' noun | 'v' verb | ' r' adv
    
#     #print("WordNet lemmatization: " + lemmas.__str__())
#     return lemmas

def remove_stopwords(words):
    stoplist = stopwords.words('english')
    #print(stoplist)
    return [w for w in words if w not in stoplist]

def remove_punctuation(words):
    punctuation = set(string.punctuation)
    return [w for w in words if  w not in punctuation]

def get_n_frequent_words(lemmas, n = 10):
    string = ' '.join(lemmas)
    frec = nltk.FreqDist(nltk.word_tokenize(string))
    print('---------')
    print('Top ' + str(n) + ' most common: ' + frec.most_common(n).__str__())
    return string

def get_n_rare_words(lemmas, n = 10):
    string = ' '.join(lemmas)
    frec = nltk.FreqDist(nltk.word_tokenize(string))
    print('---------')
    print('Top ' + str(n) + ' least common: ' + list(frec.keys())[-n:].__str__())

def POS_tag(lemmas):
    pos_mapping = {'NOUN': 'n', 'ADJ': 'a', 'VERB': 'v', 'ADV': 'r', 'ADP': 'n', 'CONJ': 'n', 'PRON': 'n', 'NUM': 'n', 'X': 'n' }
    wordnet = WordNetLemmatizer()
    tagged_lemmas = pos_tag(lemmas, tagset='universal')
    print(lemmas)
    lemmas = [wordnet.lemmatize(word, pos=pos_mapping[tag]) for (word,tag) in tagged_lemmas if tag in pos_mapping.keys()]
    print(lemmas)
    # NER ?????
    
def parse_and_chunk(lyric):
    lyric = lyric.replace("\n\n", '. ')
    lyric = lyric.replace("\n", '. ')
    pattern = """NP: {<PRON><ADJ><NOUN>+} 
                 {<DET>?<ADV>?<ADJ|NUM>*?<NOUN>+}
                 """
    NPChunker = RegexpParser(pattern)
    lyric_pos = (pos_tag(word_tokenize(lyric),  tagset='universal'))

    chunks_np = NPChunker.parse(lyric_pos)
    print(extractTrees(chunks_np, 'NP'))
    print(extractStrings(chunks_np))
    #print(chunks_np)
    chunks_np.draw()

def extractTrees(parsed_tree, category='NP'):
    return list(parsed_tree.subtrees(filter=lambda x: x.label()==category))

def extractStrings(parsed_tree, category='NP'):
    return [" ".join(word for word, pos in vp.leaves()) for vp in extractTrees(parsed_tree, category)]
    
# def vectorize(lyric):
#     vectorizer = CountVectorizer(analyzer = "word", max_features = 5000) 
#     vectors = vectorizer.fit_transform([lyric])
#     print(vectors.toarray())
#     print(vectorizer.get_feature_names())
#     #distance


# def bigram_vectors(lyric):
#     vectorizer = CountVectorizer(analyzer="word", stop_words='english', ngram_range=[2,2]) 
#     vectors = vectorizer.fit_transform([lyric])
#     print(vectors.toarray())
#     print(vectorizer.get_feature_names())

# def tfidf_vector(lyric):

#     vectorizer = TfidfVectorizer(analyzer="word", stop_words='english')
#     vectors = vectorizer.fit_transform([lyric])
#     vectorizer.get_feature_names()
#     print(vectors.toarray())
#     cosine_similarity(vectors)
#     query = ["sex blood"]
#     #cosine_similarity
#     vector_query = vectorizer.transform(query)
#     print(cosine_similarity(vector_query, vectors))

def preprocess(lyric):
    lyric = lyric.lower()
    lyric = lyric.replace("\r", '\n')
    lyric = lyric.replace("\r\n", '\n')
    lyric = lyric.replace("\r\n", '\n')
    words = get_words(lyric)
    lemmas = lemmatize(words)
    lemmas = remove_stopwords(lemmas) # i, you, me...
    #before this i should use punctuation for something
    clean_lemmas = remove_punctuation(lemmas) # i, you, me...
    
    string = get_n_frequent_words(clean_lemmas)
    get_n_rare_words(clean_lemmas)
    
    #Syntactic Processing
    POS_tag(clean_lemmas)
    return clean_lemmas, string


#lyric = open_lyric('')
#lyric = open_lyric('./lyrics_lyricwikia/happy_The.Red.Hot.Chili.Peppers_Blood.Sugar.Sex.Magik')
lyric = open_lyric('./lyrics_lyricwikia/angry_Marilyn.Manson_Sweet.Dreams.')
#lyric = open_lyric("./lyrics_lyricwikia/happy_Queen_Thank.God.It's.Christmas")
print(lyric)
#lemmas, string = preprocess(lyric)
parse_and_chunk(lyric)
#stem(lyric, 'lancaster')