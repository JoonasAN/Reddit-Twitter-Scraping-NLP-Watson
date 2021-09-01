#-------------------------------------------------------------------------
# Import libraries
#-------------------------------------------------------------------------

from re import I, T
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import ClassificationsOptions, Features, EntitiesOptions, KeywordsOptions, SentimentOptions, SummarizationOptions, \
    SyntaxOptions, SyntaxOptionsTokens, CategoriesOptions, ConceptsOptions, \
    EmotionOptions, MetadataOptions, RelationsOptions, SemanticRolesOptions
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
#Methods for IBM Watson Natural Language Understanding
#-------------------------------------------------------------------------

with open('naturallanguageunderstanding.json', 'r') as credentialsFile:
    credentials1 = json.loads(credentialsFile.read())

NLU_API_KEY_ID = credentials1.get('apikey')
NLU_URL = credentials1.get('url')

nlu_authenticator = IAMAuthenticator(NLU_API_KEY_ID)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=nlu_authenticator
)

natural_language_understanding.set_service_url(NLU_URL)


def analyse_NLU(df, saveFile:bool):
    """
    Get Watson Natural Language Understanding insights as json-file.
    - if you are using to get insight in multiple samples use: sampleRun = True
    """

    # Make new columns for dataframe
    #df = df.assign(keyword_text=pd.Series(np.ma.zeros(len(df['text']))).values, 
    #            sentiment_label=pd.Series(np.ma.zeros(len(df['text']))).values, 
    #            sentiment_score=pd.Series(np.ma.zeros(len(df['text']))).values, 
    #            relevance=pd.Series(np.ma.zeros(len(df['text']))).values)


    #Iterate through text and index
    json_nlu = {"data": []}

    for index, text in tqdm(df['text'].iteritems(), desc="Analysing Data", total=len(df)):

        #Pass a single row to NLU (one by one): all features
        response = natural_language_understanding.analyze(text=text, 
                                                        language="en",
                                                        return_analyzed_text = True,
                                                        features=Features(entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
                                                        keywords=KeywordsOptions(emotion=True, sentiment=True,limit=2),
                                                        sentiment=SentimentOptions(document=True),
                                                        semantic_roles=SemanticRolesOptions(limit=2),
                                                        summarization=SummarizationOptions(limit=2),
                                                        categories=CategoriesOptions(explanation=True, limit=2),
                                                        relations=RelationsOptions(),
                                                        #metadata=MetadataOptions(),
                                                        #classifications=ClassificationsOptions(),
                                                        emotion=EmotionOptions(document=True),
                                                        concepts=ConceptsOptions(limit=2),
                                                        syntax=SyntaxOptions(sentences=True,
                                                                            tokens=SyntaxOptionsTokens(
                                                                            lemma=True,
                                                                            part_of_speech=True,)))).get_result()
        
        #json_frame= {"id": df.loc[index,"id"], "response": response}

        # add json objects to structure

        # make id for object from dataframe id
        try:
            json_id={"id": int(df.loc[index,"id"])}
        except ValueError:
            json_id={"id": str(df.loc[index,"id"])}
        # update response to id
        json_id.update(response)
        # append json struct to list
        json_nlu['data'].append(json_id)

        
       # json_nlu["data"].append(response) # append id also 
        
        # take features and place them to the corresponding column and row
            # We don't make csv file now because it would be huge.
        
    if saveFile == True:
        # dump list of json structs to json file 
        with open('./data/data_nlu.json', 'w') as file:
            json.dump(json_nlu, file, indent=4)
    return(json_nlu)


def main():
    df = pd.read_csv('./data/'+input("Give csv data: ")+'.csv', sep = ',')
    analyse_NLU(df,saveFile=True)
    return(0)

if __name__=="__main__":
    main()