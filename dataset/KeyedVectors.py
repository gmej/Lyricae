
# coding: utf-8

# In[1]:


get_ipython().system('pip install gensim')


# In[2]:


import pandas as pd
import numpy as np


# In[3]:


from gensim.models import KeyedVectors
WORD2VEC_PATH = 'Word2Vec/glove.w2vformat.6B.100d.txt'

wordembedding = KeyedVectors.load_word2vec_format(WORD2VEC_PATH)


# In[4]:


#CELL FOR TESTING DATAFRAME STRUCTURE

list = ["this", "that", "man", "woman", "apple", "pear", "C"]
new_list = []

#Clean words that are not in vocabulary
for word in list:
    if word in wordembedding.vocab:
        new_list.append(word)
print(list)
print(new_list)
list = new_list

length = len(list)
similarities_array = np.zeros(shape=(length, length))
i = 0
for word in list:
    similarities = []
    for word2 in list:
        similarities.append(wordembedding.similarity(word, word2))
    similarities_array[i] = similarities
    i += 1
similarities_df = pd.DataFrame(similarities_array, columns=list, index=list)
print(similarities_df["this"]["woman"])
print(similarities_df)


# In[5]:


#CELL FOR CHECKING VOCABULARY
emotions = ["happy", "sad", "angry", "relaxed"]

existing_set = set()
not_existing_set = set()
for emotion in emotions:
    emotion_df = pd.read_csv("dataframes/" + emotion + "_unigram_data.csv") # read csv
    list = emotion_df['word'].tolist() # get words
    for word in list:
        if word in wordembedding.vocab:
            existing_set.add(word)
        else:
            not_existing_set.add(word)
print(len(existing_set))
print(existing_set)
print(len(not_existing_set))
print(not_existing_set)


# In[17]:


emotions = ["happy", "sad", "angry", "relaxed"]
for emotion in emotions:
    emotion_df = pd.read_csv("dataframes/" + emotion + "_unigram_data.csv") # read csv
    initial_list = emotion_df['word'].tolist() # get words
    
    #Clean words that are not in vocabulary
    word_list = []
    for word in initial_list:
        if word in wordembedding.vocab:
            word_list.append(word)
    length = len(word_list)
    similarities_array = np.zeros(shape=(length, length))
    i = 0
    for word in word_list:
        similarities = []
        for word2 in word_list:
            similarities.append(wordembedding.similarity(word, word2))
        similarities_array[i] = similarities
        i += 1
    similarities_df = pd.DataFrame(similarities_array, columns=word_list, index=word_list)
    #similarities_df.index.name = 'word'
    #similarities_df.set_index('word', inplace = True)
    print(similarities_df)
    
    similarities_df.to_csv("dataframes/" + emotion + "_similarities.csv")


# In[7]:


angry_sims = pd.read_csv("dataframes/angry_similarities.csv") # read csv
print(angry_sims)


# In[8]:


wordembedding.similarity("'s", "n't")

