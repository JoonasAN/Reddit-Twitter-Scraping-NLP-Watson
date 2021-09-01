import cmas
import pandas as pd

def main():
    twitterData = './data/'+input("Give name of Twitter data: ")+'.csv'
    redditData = './data/'+input("Give name of Reddit data: ")+'.csv'
    cmas.merge_data(twitterData,redditData)

if __name__=="__main__":
    main()