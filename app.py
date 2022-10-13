import boto3
import json
from flask import request, Flask, render_template

def langaugeTrans(language):
    padrao = "Idioma: "
    if language == "pt":
        return padrao + "Português"
    elif language == "de":
        return padrao + "Alemão"
    elif language == "en":
        return padrao + "Inglês"
    elif language == "es":
        return padrao + "Espanhol"
    elif language == "it":
        return padrao + "Italiano"
    elif language == "fr":
        return padrao + "Francês"
    elif language == "ja":
        return padrao + "Japonês"
    elif language == "ko":
        return padrao + "Coreano"
    elif language == "hi":
        return padrao + "Hindi"
    elif language == "ar":
        return padrao + "Árabe"
    elif language == "zh":
        return padrao + "Chinês - Simplificado"
    elif language == "zh-TW":
        return padrao + "Chinês - Tradicional"

def sentimentTrans(sentiment):
    padrao = "Sentimento Geral: "
    if sentiment == "POSITIVE":
        return padrao + "Positivo"
    elif sentiment == "NEGATIVE":
        return padrao + "Negativo"
    elif sentiment == "NEUTRAL":
        return padrao + "Neutro"
    elif sentiment == "MIXED":
        return padrao + "Misto"

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


app = Flask(__name__,template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def test():
    output = request.get_json() 
    result = json.loads(output)
    languageTxtUser, sentimentTxtUser = sentimentAnalisis(result['txtUser'])

    if (languageTxtUser == '') & (sentimentTxtUser == ''):
        return ['Falha na compreensão do idioma. Tente novamente.', '']
        

    languageTxtUser = langaugeTrans(languageTxtUser)
    sentimentTxtUser = sentimentTrans(sentimentTxtUser)

    info = [languageTxtUser, sentimentTxtUser]

    return info


if __name__ == "__main__":
    app.run(debug=True)

#https://softexsentimentanalysis.herokuapp.com/