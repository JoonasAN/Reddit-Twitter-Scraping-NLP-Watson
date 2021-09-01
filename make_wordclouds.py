import json
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import numpy as np
from nltk.corpus import stopwords
import json



def make_wordclouds(data):
    """
    Makes WordClouds and saves them as png images to the working folder.
    Also returns wordclouds and strings used in making them.
    
    - input: json-file from Watson_NLU.py.
    """
    verbs = []
    nouns = []
    adj = []
    words_l = list()

    cloud_mask = np.array(Image.open("./figures/cloud_mask.png"))

    for response in data['data']:
        # look for verbs, nouns and adjectives from tokens of text
        
        for i in response['syntax']['tokens']:
            if i['part_of_speech'] == 'VERB':
                verbs.append(i['text'])
   
        for i in response['syntax']['tokens']:
            if i['part_of_speech'] == 'NOUN':
                nouns.append(i['text'])
                
        for i in response['syntax']['tokens']:
            if i['part_of_speech'] == 'ADJ':
                adj.append(i['text'])

            
    comment_words_verbs = ' '
    comment_words_adj = ' '
    comment_words_nouns= ' '
    #stopwords = set(STOPWORDS)

    for val in verbs:
        val = str(val)
        tokens = val.split()
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        for words in tokens:
            comment_words_verbs = comment_words_verbs + words + ' '
    

    for val in adj:
        val = str(val)
        tokens = val.split()
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        for words in tokens:
            comment_words_adj = comment_words_adj + words + ' '
    

    for val in nouns:
        val = str(val)
        tokens = val.split()
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        for words in tokens:
            comment_words_nouns = comment_words_nouns + words + ' '
    

    # generate wordclouds
    wordcloud_verbs = WordCloud(width=800, height=800,
                                background_color='black',
                                #colormap="",
                                mask=cloud_mask,
                                stopwords=stopwords.words('english'),
                                min_font_size=10,
                                max_font_size=200,
                                random_state=42).generate(comment_words_verbs).to_file("./figures/Wordcloud-Verbs.png")

    wordcloud_adj = WordCloud(width = 800, height = 800, 
                                background_color ='black', 
                                colormap="Dark2", 
                                mask=cloud_mask,
                                stopwords = stopwords.words('english'), 
                                min_font_size = 10, 
                                max_font_size=200, 
                                random_state=42).generate(comment_words_adj).to_file("./figures/Wordcloud-Adj.png")

    wordcloud_nouns = WordCloud(width = 800, height = 800, 
                                background_color ='black', 
                                colormap="Dark2_r", 
                                mask=cloud_mask,
                                collocations=False,
                                stopwords = stopwords.words('english'), 
                                min_font_size = 10, 
                                max_font_size=200, 
                                random_state=42).generate(comment_words_nouns).to_file("./figures/Wordcloud-Nouns.png")
                                
    return(wordcloud_adj, wordcloud_nouns, wordcloud_verbs)


if __name__=="__main__":
    with open('./data/data_nlu.json', 'r') as j:
        json_data = json.load(j)
        
    wc_adj, wc_nouns, wc_verb = make_wordclouds(json_data)
