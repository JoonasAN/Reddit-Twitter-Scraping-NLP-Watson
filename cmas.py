"""------------------Clean, Calculate, Merge and Sample---------------------\n
Functions to Clean, merge, sample and calculate complexity of data from both Twitter and Reddit"""

import pandas as pd
import numpy as np
import re 
import string
from tqdm import tqdm
from datetime import datetime
import json

# constants
COLS = ['id','created_utc', 'author', 'score', 'text', 'subreddit']


def sample_data(twitterFile, redditFile, size:int):
    """
    This function samples data from dataframes.

    twitterFile: dataframe to sample
    redditFile: dataframe to sample
    size: sample size
    samples: number of samples 
    """
    
    # check if files are pandas dataframes
    if isinstance(twitterFile, pd.DataFrame) and isinstance(redditFile, pd.DataFrame):
        #print("\nFiles already df")
        df1 = twitterFile
        df2 = redditFile
    else:
        #print("\nmaking dfs")
        df1 = pd.read_csv(twitterFile+'.csv', sep = ',')
        df2 = pd.read_csv(redditFile+'.csv', sep = ',')

    # make source columns
    df1['source'] = 'twitter'
    df2['source'] = 'reddit'
    # print(df2.head())
    
    # make samples
    sample1 = df1.sample(size)
    sample2 = df2.sample(size)


    return(sample1, sample2)


def merge_data(twitterFile, redditFile, path):
    """
    Returns csv of merged data.
    
    """
    # load data
    df1 = pd.read_csv(twitterFile+'.csv', sep = ',')
    df2 = pd.read_csv(redditFile+'.csv', sep = ',')

    # add source column
    df1['source'] = 'twitter'
    df2['source'] = 'reddit'

    # merge samples
    df3 = df1.append(df2,ignore_index=True)

    # save data
    with open(path+input("\nName the merged CSV-file: ")+'.csv', 'a' ,encoding='utf-8') as csvFile:
        df3.to_csv(csvFile, mode='a', index=False, encoding="utf-8", sep=',')

def calculate_complexity(data):
    """Calculates complexity based on 1000 most used words, returns data appended with complexity column"""
    # load 1000 most common words in english
    with open('./1000most_common_words.txt') as f:
        most_common_words = f.read().splitlines() 
    
    # init complexity
    complexities = []

    punct = string.punctuation+'—'
    
    for i in tqdm(data.index,desc='Counting Complexity'):
        complexity = float()
        common_words = int()

        # choose text one row at a time
        text = data.loc[i,'text']

        # remove punctuation from text
        text = remove_punct(text)

        # spit text into list of words
        words_in_txt = text.split()

        # make words in lowercase
        for t in range(len(words_in_txt)):
            words_in_txt[t] = words_in_txt[t].lower()  
        #print(words_in_txt)

        # count how many of the used words are in most common words.
        for word in words_in_txt:
            if word in most_common_words:
                common_words += 1
                #print(f"{word:8} is in 1000 most common words")

        # calculate complexity
        complexity = 1 - common_words/len(words_in_txt)

        # append complexity to to list
        complexities.append(complexity)

        #print(f"\nindex = {i}, complexity = {common_words} / {len(words_in_txt)} = {complexity}\n")

    data['complexity'] = complexities

    save = input("\nSave data with complexity as CSV? y/n: ")

    if save == 'y':
        file = input("\nName CSV-file: ")
        with open('./data/'+file+'.csv', 'w', encoding='utf-8') as csvFile:
            data.to_csv(csvFile, index=False, encoding="utf-8")
    else:
        print("\nYou did not save.")
    return(data)

def replace_spl_char(text):
    punct = string.punctuation+'—'
    # replace special character with a whitespace if next character is not a whitespace
    try:
        for index, char in enumerate(text):
            if index != len(text)-1:
                next_char = text[index+1]
            if char in punct:
                if next_char != ' ':
                    text = text.replace(char, " ")
                    #print('replaced', char)
            #print(text)
    except TypeError:
        print(f"\nFailed because text was: {text} | {type(text)}")
    return text

def remove_punct(text):
    # discard all punctuations, and add whitespace if next character is not whitespace
    text = replace_spl_char(text)
    punct = string.punctuation+'—'
    try:
        text_nopunct = "".join([char for char in text if char not in punct])
    except TypeError:
        print(f"\nFailed because text was: {text} | {type(text)}")
    #print("\n"+text_nopunct)
    return text_nopunct

def reform_data(data, file):
    """Change column order, format time, rename column(s) and remove nan values from text column"""
    try:
        data = data[COLS]
        # format time in reddit
        data['created_utc'] = data['created_utc'].apply(lambda x: datetime.utcfromtimestamp(x))
    except KeyError:
        # go here if twitter data
        print('Failed, changing column names...\n')
        data = data.rename(columns={'created_at':'created_utc'})
        # format time as in reddit
        data['created_utc']=data['created_utc'].apply(lambda x: datetime.strftime(datetime.strptime(x,'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S'))
        #print(data)
        # add empty subreddit column
        data['subreddit'] = np.nan

    # remove rows with empty text
    data=data.dropna(subset=['text'])

    # Save data
    save = input("\nSave reformed data? y/n: ")
    if save == 'y':
        with open('./data/'+file+'.csv', 'w', encoding='utf-8') as csvFile:
            data.to_csv(csvFile, mode='a', columns=COLS, index=False, encoding="utf-8")
    print(data.head(1))

    return(data)

def test(data):
    # format time in reddit
    data['created_utc'] = data['created_utc'].apply(lambda x: datetime.utcfromtimestamp(x)) 
    print(data)

    # format twitter time as in reddit
    data['created_utc']=data['created_utc'].apply(lambda x: datetime.strftime(datetime.strptime(x,'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S'))
    print(data)

def test2(data2):
    # load jsons
    #with open("./data/json_test.json", "r") as file:
    #    data = json.load(file)

    
    #with open("./data/test.json", "r+") as file:
    #    data2 = json.load(file)
    
    #df = pd.read_csv("./data/data_tone.csv")
    #df = df.head(10)

    data2 =[{
        "name" : "sathiyajith",
        "rollno" : 56,
        "cgpa" : 8.6,
        "phonenumber" : "9976770500"
        },
        {
        "name" : "sathiyajith",
        "rollno" : 56,
        "cgpa" : 8.6,
        "phonenumber" : "9976770500"
        }]

    df=pd.DataFrame({"id": ["h4l3q2a",11,22,33,44,55,66,77,88,99]})

    # take all things in list in json and append them to list in other json

    # update id on top
    l = []
    for i, d in enumerate(data2):
        #l.append(d)
        try:
            updict={"id": int(df.loc[i,"id"])}
        except ValueError:
            updict={"id": str(df.loc[i,"id"])}
        print(d)
        updict.update(d)
        l.append(updict)

    print(json.dumps(l,indent=4))


    #print(len(data['data']))
    # save file
    #with open('./data/test1.json', 'w') as file:
    #    json.dump(l, file, indent=4)

  

if __name__ == "__main__":
    #d = {'text': ['An old silent pond\nA frog jumps into the pond-\nSplash! Silence again.', 'A world of dew,\nAnd within every dewdrop\nA world of struggle.','The light of a candle\nIs transferred to another candle—\nSpring twilight']}
    #data = pd.DataFrame(data=d)
    #data = pd.read_csv('./data/'+input("\nGive Name of data: ")+'.csv')
    #data = reform_data(data, file='reddit_data_fixed')
    #datac = calculate_complexity(data)
    #print(datac.head(1))
    #replace_spl_char(data)

    #data1 = pd.read_csv('./data/twitter_data_cmplx.csv')
    #data2 = pd.read_csv('./data/reddit_data_cmplx.csv')
    #sample_data(data1,data2,100)
    #test(data1)

    
    
    #with open('./data/test1.json', 'w') as file:
    #    json.dump(dictionary, file, indent=4)
    test2()