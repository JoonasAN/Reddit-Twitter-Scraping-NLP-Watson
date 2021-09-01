import cmas
import twitter_search
import reddit_search
from Watson_NLU import *
from Watson_Tone import *
from tqdm import tqdm
import pandas as pd

def analyze_sampleTone(data1, data2):

    tones = pd.DataFrame()

    for i in tqdm(range(15), desc="Sample analysis"):
        # get samples
        sample1, sample2 = cmas.sample_data(data1,data2,50)

        # drop sample from dataframe
        data1 = data1.drop(sample1.index)
        data2 = data2.drop(sample2.index)

        # merge samples
        sample = sample1.append(sample2,ignore_index=True)

        # analyze tone
        tones=tones.append(analyse_tone(sample,False,False),ignore_index=True)
        
        # safe save just in case
        with open('./data/safe_tone.csv', 'a', encoding='utf-8') as csvfile:
            tones.to_csv(csvfile, index=False, encoding="utf-8")
        #tones = tones.append(sample,ignore_index=True)

        #print(tones1.head(1))
    #print(tones1.shape)
    #print(tones2.shape)

    
    print(tones)

    #save = input("\nSave merged data with tones as CSV? y/n: ")
    #if save == 'y':
    file = input("\nName the CSV-file: ")
    with open('./data/'+file+'.csv', 'w', encoding='utf-8') as csvfile:
        tones.to_csv(csvfile, index=False, encoding="utf-8")

def analyse_sampleNLU(data1, data2, loopCount):
    json_file = {'data': []}

    for i in tqdm(range(loopCount), desc="Sample analysis"):
        
        # get samples
        sample1, sample2 = cmas.sample_data(data1,data2,50)

        # drop sample from dataframe
        data1 = data1.drop(sample1.index)
        data2 = data2.drop(sample2.index)

        # analyse data
        json_file1 = analyse_NLU(data1,False)
        json_file2 = analyse_NLU(data2,False)

        # take all things in list in json and append them to list in other json
        for i in range(len(json_file1['data'])):
            json_file['data'].append(json_file1['data'][i])
        for i in range(len(json_file2['data'])):
            json_file['data'].append(json_file2['data'][i])

    # save file
    with open('./data/'+input("Name JSON-file: ")+'.json', 'w') as file:
        json.dump(json_file, file, indent=4)


        

        
    
        
def main():
    

    #data1 = pd.read_csv('./data/'+input("\nGive Name of data: ")+'.csv')
    #data1 = cmas.reform_data(data1, file='reddit_data_fixed')
    #data1 = cmas.calculate_complexity(data1)

    #data2 = pd.read_csv('./data/'+input("\nGive Name of data: ")+'.csv')
    #data2 = cmas.reform_data(data2, file='reddit_data_fixed')
    #data2 = cmas.calculate_complexity(data2)


    data1 = pd.read_csv('./data/twitter_data_cmplx.csv')
    data2 = pd.read_csv('./data/reddit_data_cmplx.csv')
    analyze_sampleTone(data1, data2)

if __name__=="__main__":
    main()