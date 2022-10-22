import boto3
import json
from flask import request, Flask, render_template
from data import dados

#TRANSLATE LANGUAGE INFORMATION
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


#TRANSLATES FEELING INFORMATION
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

#IDENTIFIES LANGUAGE AND FEELING
def sentimentAnalisis(txt):

    #CONNECT WITH AMAZON COMPREHEND SERVICE
    comprehend = boto3.client(service_name='comprehend', region_name=dados.REGION_NAME, aws_access_key_id=dados.AWS_ACCESS_KEY_ID, aws_secret_access_key=dados.AWS_SECRET_ACCESS_KEY)

    #DETECT THE LANGUAGE OF THE TEXT
    lan = json.dumps(comprehend.detect_dominant_language(Text = txt), sort_keys=True, indent=4)
    
    lanAux = json.loads(lan)
    lanList = list(lanAux.items())
    languageTxtUser = lanList[0][1][0]['LanguageCode']

    #DETECTS THE FEELING OF THE TEXT
    sentiment = json.dumps(comprehend.detect_sentiment(Text=txt, LanguageCode=str(languageTxtUser)), sort_keys=True, indent=4)
    sentimentAux = json.loads(sentiment)
    sentimentList = list(sentimentAux.items())
    sentimentTxtUser = sentimentList[1][1]

    return languageTxtUser, sentimentTxtUser


app = Flask(__name__,template_folder='templates')

#SET THE TEMPLATE FOR THE DEFAULT ROUTE
@app.route('/')
def index():
    return render_template('index.html')

#SET THE TEMPLATE TO THE SPECIFIED ROUTE
@app.route('/test', methods=['POST'])
def test():
    output = request.get_json() 
    result = json.loads(output)
    languageTxtUser, sentimentTxtUser = sentimentAnalisis(result['txtUser'])

    #ANALYZE IF THE ENTRY IS VALID
    if (languageTxtUser == '') & (sentimentTxtUser == ''):
        return ['Falha na compreensão do idioma. Tente novamente.', '']
        

    languageTxtUser = langaugeTrans(languageTxtUser)
    sentimentTxtUser = sentimentTrans(sentimentTxtUser)

    info = [languageTxtUser, sentimentTxtUser]

    return info


#EXECUTE MAIN FUNCTION
if __name__ == "__main__":
    app.run(debug=True)
