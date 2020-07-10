from wordfreq import zipf_frequency
import pandas as pd


DATAFRAME_FOLDER_PATH = "./dataframes/"
THRESHOLD = 5.3
sentiments = ["happy", "relaxed", "angry", "sad",]

def delete_not_english_words(sentiment, save=False):
    """ print("\n----------------------\n")
    print(sentiment) """
    
    dataframe_path = DATAFRAME_FOLDER_PATH + sentiment + "_unigram_data.csv"
    df = pd.read_csv(dataframe_path,
        dtype={'word': str, 'totalRepetitions': int, 'fileOcurrences': int, 'weight': float})
    
    unigrams_list = df['word'].tolist()
    weights_list = df['weight'].tolist()
    
    """print(df.nlargest(30, 'weight'))
    print(df.size)
    print("->>>") """
    
    indexes = []
    i=0
    for word in unigrams_list:
        if(zipf_frequency(word, 'en') < THRESHOLD and weights_list[i]<100):
            indexes.append(i)
        i+=1
    df = df.drop(df.index[indexes])
    #print(df.size)
    if(save):
        df.to_csv(dataframe_path)
    
    
    
def main():
    for sent in sentiments:
        delete_not_english_words(sent, save=True)

if __name__ == "__main__":
    main()