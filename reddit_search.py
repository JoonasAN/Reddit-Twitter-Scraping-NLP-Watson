from psaw import PushshiftAPI
from datetime import datetime
import pandas as pd
import numpy as np
import sys
from tqdm import tqdm

def search_data(limit, file):

    # make a submission generator
    api_submission_generator = api.search_submissions(q=search_phrase, 
                                                        limit=limit,
                                                        filter=['id', 'selftext', 'subreddit', 'score', 'author', 'created'])

    # make a comment generator
    api_comment_generator = api.search_comments(q=search_phrase, 
                                                limit=limit,
                                                filter=['id', 'body', 'subreddit', 'score', 'created_utc', 'author'])

    # change row where to print
    sys.stdout.write("\n")
    sys.stdout.flush()

    # Get data and make dataframe
    submissions = pd.DataFrame([submission.d_ for submission in tqdm(api_submission_generator, total=limit, desc='Searching Submissions')])

    # change row where to print
    sys.stdout.write("\n")
    sys.stdout.flush()

    comments = pd.DataFrame([comment.d_ for comment in tqdm(api_comment_generator, total=limit, desc='Searching Comments')])

    # remove pet problem rows (way too much animal pain posts)
    #df_submissions = df_submissions.loc[~df_submissions['selftext'].str.contains('"my dog"|"my cat"|"my horse"')]
    #df_comments = df_comments.loc[~df_comments['body'].str.contains('dog|cat|horse')]

    # make new dataframes and rename column name to get them on the same column
    submissions = submissions[['id', 'selftext', 'subreddit', 'score', 'created_utc', 'author']].rename(columns={"selftext": "text"})
    comments = comments[['id', 'body', 'subreddit', 'score', 'created_utc', 'author']].rename(columns= {"body": "text"})
    
    # merge dataframes as new dataframe
    frames = [submissions, comments]
    df_subcom = pd.concat(frames)

    # change created_utc format
    df_subcom['created_utc'] = df_subcom['created_utc'].apply(lambda x: datetime.utcfromtimestamp(x)) 

    # drop duplicates
    df_subcom.drop_duplicates(subset='text')
     
    # reset index of dataframe
    df_subcom = df_subcom.reset_index(drop=True)

    # save df as csv file
    with open('./data/'+file+'.csv', 'a' ,encoding='utf-8') as csvFile:
        df_subcom.to_csv(csvFile, mode='a', index=False, encoding="utf-8", sep=',')

    # change row where to print
    sys.stdout.write("\n")
    sys.stdout.flush()
    return(1)

def main():

    search_data(file = input("\nName CSV-file without extension: "), limit=int(input("\nGive max limit of submissions and comments searched.\nNone if no limit needed.\n> ")))
    #df = remove_excess(submissions, comments)
    return(0)
    

if __name__ == "__main__":
    # Give Keywords
    search_phrase = '(("back pain")|lumbago|sciatica|backache|("slipped disk"))&(((self)&(care|treatment))|alleviate|((in|at)&(home))|prevent|improve)'

    api = PushshiftAPI()
    main()

    # Checks if there are shards down - effects search results
    #print(api.metadata_.get('shards'))