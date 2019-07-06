from flask import Flask, request
from twilio.twiml.voice_response import Gather, VoiceResponse, Say
import json
import os
import requests

app = Flask(__name__)


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

    print(''.join(transcripts))

    return ''.join(transcripts)

if __name__ == "__main__":
    app.run()
