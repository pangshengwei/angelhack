from flask import Flask, request
from twilio.twiml.voice_response import Gather, VoiceResponse, Say
import json
import os
import requests
from ibm_watson import NaturalLanguageUnderstandingV1, ToneAnalyzerV3
from ibm_watson.natural_language_understanding_v1 \
import Features, EntitiesOptions, KeywordsOptions
import urllib
global call_results
from ibm_watson import SpeechToTextV1
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

call_results = ''

app = Flask(__name__)
api = Api(app)
result = {}
CORS(app)

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    iam_apikey='7bRw7H8zA9Dp4iFRcuZ77yPrw6kpOM-PbUBqV-buDGy7',
    url='https://gateway.watsonplatform.net/natural-language-understanding/api')

@app.route("/answer", methods=['GET', 'POST'])
def record():

    response = VoiceResponse()
    #gather = Gather(input='speech', action='/completed')
    #gather.say('Welcome to Twilio, please tell us why you\'re calling')
    #response.append(gather)
    response.say('Hello this is Eva, you have reached nine nine five. Please state your name, location and describe your situation after the beep.')
    response.record(action="/recording")
    response.hangup()

    return str(response)


@app.route("/recording", methods=['GET', 'POST'])
def recording():
    recording_url = request.values.get("RecordingUrl", None)
    print(recording_url)

    response = VoiceResponse()
    #response.say("Thanks for the response. This is what you said.")
    #response.play(recording_url)
    response.say("Thank you, our responders have taken note of your call")

    return str(response)

@app.route("/callback", methods=['POST', 'PUT'])
def callback():
    global call_results
    add_ons = json.loads(request.values['AddOns'])

    if 'ibm_watson_speechtotext' not in add_ons['results']:
        return 'Add Watson Speech to Text add-on in your Twilio console'

    payload_url = add_ons["results"]["ibm_watson_speechtotext"]["payload"][0]["url"]

    account_sid = 'AC83a61ef5d6aab46c4146c60d4fffe598'
    auth_token = '35e4cc8c8e57d80f9df42d8522263caf'

    resp = requests.get(payload_url, auth=(account_sid, auth_token)).json()
    results = resp['results'][0]['results']

    transcripts = map(lambda res: res['alternatives'][0]['transcript'], results)

    call_results = ''.join(transcripts)
    response = natural_language_understanding.analyze(
                text=call_results,
                features=Features(
                    entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
                    keywords=KeywordsOptions(emotion=True, sentiment=True,
                                             limit=2))).get_result()
    print(json.dumps(response, indent=2))

    return ''.join(transcripts)

def sentiment_analysis(text):
    tone_analyzer = ToneAnalyzerV3(
        version='2018-09-19',
        iam_apikey='z4eyiTUomZQHQPbAgQ79ilFlned-Z2fPYNqZ3K2YC9iE',
        url='https://gateway.watsonplatform.net/tone-analyzer/api'
    )

    tone_analysis = tone_analyzer.tone({'text': text}, content_type='application/json').get_result()

    print(json.dumps(tone_analysis, indent=2))

def google_maps(address):
    #teststreet= 'Nicole+Highway,+SG'
    #teststreet2= 'Nicole+Highway'

    #url = 'https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyCBdqIhRDqVhAefF9jDhRhslerC9D-I9xM'
    url2 = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + address +'&key=AIzaSyCBdqIhRDqVhAefF9jDhRhslerC9D-I9xM'
    contents = urllib.request.urlopen(url2).read()
    j = json.loads(contents.decode("utf-8"))
    lat = j['results'][0]['geometry']['location']['lat']
    long = j['results'][0]['geometry']['location']['lng']
    #print(lat)
    #print(long)
    return (lat,long)

def demo2():

    global call_results

    text = 'Hi, my name is Geoffrey Martin. I am located at Nicoll Highway. There has been a tunnel collapse and I see four casualties at the end of the tunnel!'
    sentiment = sentiment_analysis(text)
    call_results = text
    response = natural_language_understanding.analyze(text=call_results,features=Features(
                                                                            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
                                                                            keywords=KeywordsOptions(emotion=True, sentiment=True, limit=2))).get_result()
    response = json.dumps(response, indent=2)
    result = {}
    nlp = json.loads(response)
    result['incident_no'] = 201907061
    result['person'] = nlp['entities'][0]['text']
    result['location'] = nlp['entities'][1]['text']
    result['disaster_type'] = nlp['keywords'][0]['text']
    result['sentiment'] = 'fear'
    result['remarks'] = 'I see four casualties'
    print(result)
    return result

import operator
def demo():

    global call_results
    data = natural_language_understanding.analyze(text=call_results,features=Features(
                                                                            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
                                                                            keywords=KeywordsOptions(emotion=True, sentiment=True, limit=2))).get_result()
    callData = {'incident_no': 201907061, 'name': [], 'location': [], 'disaster_type': [], 'sentiment': None, 'remarks': []}

    for entity in data['entities']:
        if entity['type'] == "Person":
            callData["name"].append(entity['text'])
        elif entity['type'] == "Quantity":
            callData["remarks"].append(entity['text'])
        else:
            callData["location"].append(entity['text'])

    sentiment = -1

    if sentiment < 0:
        callData["sentiment"] = "horrified"
    else:
        callData["sentiment"] = "scared"

    keywordList = []
    for keyword in data['keywords']:
        keywordList.append(keyword['text'])

    keywordList = ''.join(keywordList)
    keywordList = keywordList.replace('HESITATION ', '')
    callData['remarks'] = keywordList

    return callData


class Employees(Resource):
    def get(self):
        return {'employees': [{'id':1, 'name':'Balram'},{'id':2, 'name':'Tom'}]}

class Event(Resource):
    def get(self):
        print(result)
        res = [val for key, val in demo2().items()]
        #location = demo2().items()['location']
        location = 'Nicole+Highway'
        lat, long = google_maps(location)
        print(res + [lat] + [long])
        return res + [lat] + [long]

api.add_resource(Employees, '/employees')
api.add_resource(Event, '/event')

if __name__ == "__main__":
    app.run()
