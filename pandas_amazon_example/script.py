import pandas as pd
import gzip
import PIL
import itertools
import matplotlib.pyplot as plt
import re
from wordcloud import WordCloud



stop_words =['i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself',
            'yourselves','he','him','his','himself','she','her','hers','herself','it','its','itself',
            'they','them','their','theirs','themselves','what','which','who','whom','this','that',
            'these','those','am','is','are','was','were','be','been','being','have','has','had',
            'having','do','does','did','doing','a','an','the','and','but','if','or','because','as',
            'until','while','of','at','by','for','with','about','against','between','into','through',
            'during','before','after','above','below','to','from','up','down','in','out','on','off',
            'over','under','again','further','then','once','here','there','when','where','why','how',
            'all','any','both','each','few','more','most','other','some','such','no','nor','not',
            'only','own','same','so','than','too','very','s','t','can','will','just','don','should',
            'now','uses','use','using','used','one','also']

 
def parse(path):
    g = gzip.open(path, 'rb')
    for l in g:
        yield eval(l)
 
def getDF(path): 
    i = 0
    df = {}
    for d in parse(path):
        df[i] = d
        i += 1
    return pd.DataFrame.from_dict(df, orient='index')

def preprocess(data):
    reviews_tokens = []
    for review in data:
        review = review.lower() #Convert to lower-case words
        raw_word_tokens = re.findall(r'(?:\w+)', review,flags = re.UNICODE) #remove pontuaction
        word_tokens = [w for w in raw_word_tokens if not w in stop_words] # do not add stop words
        reviews_tokens.append(word_tokens)
    return reviews_tokens #return all tokens

musical_data = getDF('reviews_Musical_Instruments_5.json.gz')
office_data = getDF('reviews_Office_Products_5.json.gz')

frames = [musical_data.reviewText[:1000],office_data.reviewText[:1000]]
reviews_names = ['musical','office']

complete_data = pd.concat(frames, keys = reviews_names)
for review,name in zip(frames, reviews_names):
    raw_str = complete_data.loc[name].str.cat(sep=',')
    print(raw_str)
    wordcloud = WordCloud( max_words=1000,margin=0).generate(raw_str)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

for reviews,name in zip(frames,reviews_names):
    tokenized_reviews = preprocess(reviews) #apply the preprocess step
    reviews = list(itertools.chain(*tokenized_reviews))
    text_reviews = " ".join(reviews)
    wordcloud = WordCloud( max_words=1000,margin=0).generate(text_reviews)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    #image = wordcloud.to_image()
    #image.show()
    #image.save(name+'.bmp')
