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

app = Flask(__name__)

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
    response.say('Pang is a cocksucker.\nPress any key when finished.')
    response.record(maxLength="10", action="/recording")
    response.hangup()

    return str(response)


@app.route("/recording", methods=['GET', 'POST'])
def recording():
    recording_url = request.values.get("RecordingUrl", None)
    print(recording_url)

    response = VoiceResponse()
    response.say("Thanks for the response. This is what you said.")
    response.play(recording_url)
    response.say("Goodbye and remember that Pang loves BBC.")

    return str(response)

@app.route("/callback", methods=['POST', 'PUT'])
def callback():

    add_ons = json.loads(request.values['AddOns'])

    if 'ibm_watson_speechtotext' not in add_ons['results']:
        return 'Add Watson Speech to Text add-on in your Twilio console'

    payload_url = add_ons["results"]["ibm_watson_speechtotext"]["payload"][0]["url"]

    account_sid = 'AC7a0a2584e4228851c405d7bd74ce9f07'
    auth_token = '0f34612a29a149fe590aae5235742b41'

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

    tone_analysis = tone_analyzer.tone(
        {'text': text},
        content_type='application/json'
    ).get_result()

    print(json.dumps(tone_analysis, indent=2))

def google_maps():
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyCBdqIhRDqVhAefF9jDhRhslerC9D-I9xM'
    contents = urllib.request.urlopen(url).read()
    j = json.loads(contents.decode("utf-8"))

    return j

if __name__ == "__main__":
    app.run()
