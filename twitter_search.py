# This code searches tweets using twitter API based on search phrase

import os
import pandas as pd
import numpy as np
import tweepy
import json
import sys
from tqdm import tqdm   # imports progressbar

# init constants
PAGES = 30
PATHDATA = './data/'    # path for data folder
COLS_T = ['id', 'created_at', 'author', 'score', 'text'] #columns of the csv file

def write_tweets_30(keyword, file, **kwargs):
    """ Function returns JSON-file with all features of tweets and/or CSV-file of tweets features: creation date, text, and full_text - from last 30-days.
        To search full archive use api.search_full_archive instead of api.search_30_day.

        from_date : yyyymmddhhmm, default = None,
        to_date : yyyymmddhhmm, default = None,
        get_json : True or False, default = False,
        get_csv : True or False, default = True

        """
    from_date = kwargs.get('start_date', None)
    to_date = kwargs.get('end_date', None)
    get_json = kwargs.get('get_json', False)
    get_csv = kwargs.get('get_csv', True)

    #Twitter credentials for the app
    consumer_key = ''
    consumer_secret = ''
    access_key= ''
    access_secret = ''

    #pass twitter credentials to tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    

    # If the file exists, then read the existing data from the CSV file.
    if os.path.exists(file):
        df = pd.read_csv(file, header=0)
    else:
        df = pd.DataFrame(columns=COLS_T)

    # Make a list where to save jsons
    json_tone = {"data": []}

    #page attribute in tweepy.cursor and iteration
    for i, page in enumerate(tweepy.Cursor(api.search_30_day, 
                                                query=keyword, 
                                                environment_name='',
                                                fromDate=from_date,
                                                toDate=to_date).pages(PAGES)):
        for index, status in tqdm(enumerate(page), total=len(page), desc=f'Getting tweets from Page {i}'):
            new_entry = []

            status = status._json
            
            # add full tweet status to json file
            json_tone['data'].append(status)

            # Choose Columns that are needed in csv file,
            # and append them in "new_entry"
            new_entry += [status['id'], status['created_at'], status['user']['screen_name'], status['favorite_count']]

            try:
                new_entry.append(status['extended_tweet']['full_text'])
            except KeyError:
                try:
                    new_entry.append(status['statuses']['retweeted_status']['extended_tweet']['full_text'])
                except KeyError:
                    new_entry.append(status['text'])
                    #new_entry.append(np.nan)

            single_tweet_df = pd.DataFrame([new_entry], columns=COLS_T)
            df = df.append(single_tweet_df, ignore_index=True)

    if get_json == True:
        # dump list of json structs to json file       
        with open(PATHDATA+file+'_full.json', 'a') as f:
            json.dump(json_tone, f, indent=4)

    if get_csv == True:
        # save to csv file
        with open(PATHDATA+file+'.csv', 'a', encoding='utf-8') as csvFile:
            df.to_csv(csvFile, mode='a', columns=COLS_T, index=False, encoding="utf-8")

    lenght = len(df)

    return(lenght)


def write_tweets_full(keyword, file, **kwargs):
    """ Function returns JSON-file with all features of tweets and/or CSV-file of tweets features: creation date, text, and full_text - from Full archive.

        from_date : yyyymmddhhmm, default = None,
        to_date : yyyymmddhhmm, default = None,
        get_json : True or False, default = False,
        get_csv : True or False, default = True

        """
    from_date = kwargs.get('start_date', None)
    to_date = kwargs.get('end_date', None)
    get_json = kwargs.get('get_json', False)
    get_csv = kwargs.get('get_csv', True)

    #Twitter credentials for the app
    consumer_key = ''
    consumer_secret = ''
    access_key= ''
    access_secret = ''

    #pass twitter credentials to tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    

    # If the file exists, then read the existing data from the CSV file.
    if os.path.exists(file):
        df = pd.read_csv(file, header=0)
    else:
        df = pd.DataFrame(columns=COLS_T)

    # Make a list where to save jsons
    json_tone = {"data": []}

    #page attribute in tweepy.cursor and iteration
    for i, page in enumerate(tweepy.Cursor(api.search_full_archive, 
                                                query=keyword, 
                                                environment_name='',
                                                fromDate=from_date,
                                                toDate=to_date).pages(PAGES)):
        for index, status in tqdm(enumerate(page), total=len(page), desc=f'Getting tweets from Page {i}'):
            new_entry = []

            status = status._json
            
            # add full tweet status to json file
            json_tone['data'].append(status)

            # Choose Columns that are needed in csv file,
            # and append them in "new_entry"
            new_entry += [status['id'], status['created_at'], status['user']['screen_name'], status['favorite_count']]

            try:
                new_entry.append(status['extended_tweet']['full_text'])
            except KeyError:
                try:
                    new_entry.append(status['statuses']['retweeted_status']['extended_tweet']['full_text'])
                except KeyError:
                    new_entry.append(status['text'])
                    #new_entry.append(np.nan)

            single_tweet_df = pd.DataFrame([new_entry], columns=COLS_T)
            df = df.append(single_tweet_df, ignore_index=True)

    if get_json == True:
        # dump list of json structs to json file       
        with open(PATHDATA+file+'_full.json', 'a') as f:
            json.dump(json_tone, f, indent=4)

    if get_csv == True:
        # save to csv file
        with open(PATHDATA+file+'.csv', 'a', encoding='utf-8') as csvFile:
            df.to_csv(csvFile, mode='a', columns=COLS_T, index=False, encoding="utf-8")

    lenght = len(df)

    return(lenght)

def main():
    #lenght = write_tweets_30(search_phrase, file=input("Give filename: "))
    lenght = write_tweets_full(search_phrase, file=input("Give filename: "))
    # print completion in terminal
    sys.stdout.write(f"\nGathering Complete!\n{lenght} Tweets gathered.\n\n")
    sys.stdout.flush()

    return(0)


if __name__ == "__main__":
    # Give Keywords
    search_phrase = '(("back pain") OR lumbago OR sciatica OR backache OR ("slipped disk")) ((self (care OR treatment)) OR alleviat OR ((in OR at) home) OR prevent OR improve)'
    main()