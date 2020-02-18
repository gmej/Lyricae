

def data_clean(filename):
    f = open(filename, 'rb')
    all_words = ''
    for sentence in f.readlines():
        this_sentence = sentence.decode('utf-8')
        all_words += this_sentence
    f.close()

    #remove identifiers like chorus, verse, etc
    all_words = re.sub(r'[\(\[].*?[\)\]]', '', all_words)
    #remove empty lines
    all_words = os.linesep.join([s for s in all_words.splitlines() if s])
    
    f = open('lyrics/' + artist + '-cleaned', 'wb')
    f.write(all_words.encode('utf-8'))
    f.close()

    #amazon example
    review = review.lower() #Convert to lower-case words
    raw_word_tokens = re.findall(r'(?:\w+)', review,flags = re.UNICODE) #remove pontuaction
    word_tokens = [w for w in raw_word_tokens if not w in stop_words] # do not add stop words
    reviews_tokens.append(word_tokens)

