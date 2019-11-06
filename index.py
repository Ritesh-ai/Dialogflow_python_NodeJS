
import os
# import dialogflow
import requests
import re
import sys
import dialogflow_v2 as dialogflow
import requests
import json
import pusher
from config import *
from flask import Flask, request, jsonify, render_template
from google.oauth2 import service_account




app = Flask(__name__)

pusher_client = pusher.Pusher(
    app_id=keys.appid,
    key=keys.key,
    secret=secret.keys,
    cluster=keys.cluster,
    ssl=keys.ssl)

@app.route('/')
def index():
    return render_template('index.html')

def scrapping(text):
    data = data = {
                "names":text + " wikipedia"
                }
    r = requests.post(url = "http://127.0.0.1:8001", data = data)
    links = r.json()[1]
    str1 = "\n" 
    for i in links:
        str1+= str(i)+"\n"

    data = r.json()[0]
    if len(data) > 5:
        data1 = data[2:4]
    else:
        data1 = data
    text = " "
    for item in data1:
        text += item['text'].replace('[','@').replace(']','@')+"\n \n \n"
    import string
    exclude = set(string.punctuation)
    s = ''.join(ch for ch in text if ch not in exclude) 

    extra = "      Want to know more check out the provided links................\n" + str1 + "\n"
    
    return s + extra

def detect_intent_texts(project_id, session_id, text, language_code):
    credentials = service_account.Credentials.from_service_account_file('credentials.json')
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(project_id, session_id)
    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        # print(response,"---------------")
        # print("-------------------------------------------------------------------")
        data = str(response.query_result.intent).split("\n")[1].split(":")[1].replace('"',',').split(",")[1]
        print(data)
        if data == "tutorial":
            # print("In the call of scrapping function-----------------------")
            link = scrapping(text)
            return link
        elif data == 'Default Fallback Intent':
            return "Didn't get you. Can you please say that again."

        # print("--------------------------------------------------------------------")
        return response.query_result.fulfillment_text
f = open("history.txt","w")
@app.route('/send_message', methods=['POST'])
def send_message():
    

    sys.stdout = f
    try:
        socketId = request.form['socketId']
    except KeyError:
        socketId = ''

    print(socketId)
        
    message = request.form['message']
    print(message,"-----------------User Message")
   
    project_id = "priyanka-madam-eurstu"
    fulfillment_text = detect_intent_texts(project_id, "temp", message, 'en')
    response_text = { "message":  fulfillment_text.replace(",","\n") }
    print(fulfillment_text,"----------------Bot Message")

    pusher_client.trigger(
        'tutorial', 
        'new_message', 
        {
            'human_message': message, 
            'bot_message': fulfillment_text,
        },
        socketId
    )
                        
    return jsonify(response_text)
# run Flask app
if __name__ == "__main__":
    app.run(port = '5000')
