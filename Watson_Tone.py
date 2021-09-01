"""This script was made using IBM Watson - Tone Analyzer, and will take csv data and
code used as an example can be found at: https://github.com/IBM/use-advanced-nlp-and-tone-analyser-to-analyse-speaker-insights"""

#-------------------------------------------------------------------------
# Import libraries
#-------------------------------------------------------------------------
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ToneAnalyzerV3
import json
from tqdm import tqdm

#-------------------------------------------------------------------------
#Instantiate TA and NLP analyzers
#-------------------------------------------------------------------------

# Constants for NLU & Tone Analyzer values
NLU_API_KEY_ID = ""
NLU_URL = ""
TONE_API_KEY_ID = ""
TONE_URL = ""

#-------------------------------------------------------------------------
#Methods for IBM Watson Tone Analyser
#-------------------------------------------------------------------------

with open('toneanalyzer.json', 'r') as credentialsFile:
    credentials2 = json.loads(credentialsFile.read())

TONE_API_KEY_ID = credentials2.get('apikey')
TONE_URL = credentials2.get('url')

tone_analyzer_authenticator = IAMAuthenticator(TONE_API_KEY_ID)

tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=tone_analyzer_authenticator
)

tone_analyzer.set_service_url(TONE_URL)


def analyse_tone(df, jsonFile:bool, csvFile:bool):
    """
    Analyses tone of the text from dataframe using Watson Tone Analyzer.

    - df: dataframe to analyze
    - jsonFile: save df as JSON-file, type bool
    - csvFile: save df as CSV-file, type bool

    """

    # Make new columns for dataframe
    df = df.assign(tone_joy=pd.Series(np.ma.zeros(len(df['text']))).values, 
                    tone_sadness=pd.Series(np.ma.zeros(len(df['text']))).values, 
                    tone_tentative=pd.Series(np.ma.zeros(len(df['text']))).values, 
                    tone_analytical=pd.Series(np.ma.zeros(len(df['text']))).values,
                    tone_anger=pd.Series(np.ma.zeros(len(df['text']))).values,
                    tone_fear=pd.Series(np.ma.zeros(len(df['text']))).values,
                    tone_confident=pd.Series(np.ma.zeros(len(df['text']))).values)

    
    #--------------------------  TONE ANALYZER  ------------------------------

    # Make a list where to save jsons
    json_tone = {"data": []}

    #Iterate through text and index
    for index, text in tqdm(df['text'].iteritems(), desc='Analyzing tone', total=len(df)):

        #Pass a single review to TA (one by one):
        tone_analysis = tone_analyzer.tone({'text': text}, content_type='application/json').get_result()

        # add json objects to structure
        json_tone['data'].append(tone_analysis)

        # take tones score and place it to the corresponding column and row
    for i, ids in enumerate(tone_analysis['document_tone']['tones']):
        if tone_analysis['document_tone']['tones'][i]['tone_id'] == 'joy':
            df.loc[index,'tone_joy'] = tone_analysis['document_tone']['tones'][i]['score']
        elif tone_analysis['document_tone']['tones'][i]['tone_id'] == 'tentative':
            df.loc[index,'tone_tentative'] = tone_analysis['document_tone']['tones'][i]['score']
        elif tone_analysis['document_tone']['tones'][i]['tone_id'] == 'analytical':
            df.loc[index,'tone_analytical'] = tone_analysis['document_tone']['tones'][i]['score']
        elif tone_analysis['document_tone']['tones'][i]['tone_id'] == 'sadness':
            df.loc[index,'tone_sadness'] = tone_analysis['document_tone']['tones'][i]['score']
        elif tone_analysis['document_tone']['tones'][i]['tone_id'] == 'anger':
            df.loc[index,'tone_anger'] = tone_analysis['document_tone']['tones'][i]['score']
        elif tone_analysis['document_tone']['tones'][i]['tone_id'] == 'fear':
            df.loc[index,'tone_fear'] = tone_analysis['document_tone']['tones'][i]['score']
        elif tone_analysis['document_tone']['tones'][i]['tone_id'] == 'confident':
            df.loc[index,'tone_confident'] = tone_analysis['document_tone']['tones'][i]['score']

        #print("Added new row of tones...")
        #sys.stdout.write("\rAdding row of data: %i" % index)
        #sys.stdout.flush()

    # dump list of json structs to json file   
    if jsonFile == True:        
        with open(input("Name the json file: ")+'.json', 'a') as file:
            json.dump(json_tone, file, indent=4)

    #write csv
    if csvFile == True:
        with open(input("Name the csv file: ")+'.csv', 'a' ,encoding='utf-8') as csvfile:
            df.to_csv(csvfile, mode='a', index=False, encoding="utf-8", sep=',')
    
    return(df)

def main():
    df = pd.read_csv(input("Give csv data without extension: ")+'.csv', sep = ',')

    #get only csv file
    analyse_tone(df, jsonFile=False, csvFile=True)
    return(0)

if __name__ == "__main__":
    main()


