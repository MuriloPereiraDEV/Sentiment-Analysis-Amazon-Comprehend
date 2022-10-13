#INSTALAR AWS CLIENT COM COMANDO msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

import boto3
import json

def sentimentAnalisis(txt):
    try:
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-2')

        lan = json.dumps(comprehend.detect_dominant_language(Text = txt), sort_keys=True, indent=4)
    
        lanAux = json.loads(lan)
        lanList = list(lanAux.items())
        languageTxtUser = lanList[0][1][0]['LanguageCode']

        sentiment = json.dumps(comprehend.detect_sentiment(Text=txt, LanguageCode=str(languageTxtUser)), sort_keys=True, indent=4)
        sentimentAux = json.loads(sentiment)
        sentimentList = list(sentimentAux.items())
        sentimentTxtUser = sentimentList[1][1]

        return languageTxtUser, sentimentTxtUser
    except:
        return "", ""