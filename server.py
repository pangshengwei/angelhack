from flask import Flask
from twilio.twiml.voice_response import Gather, VoiceResponse, Say

app = Flask(__name__)


@app.route("/answer", methods=['GET', 'POST'])
def record():

    response = VoiceResponse()
    #gather = Gather(input='speech', action='/completed')
    #gather.say('Welcome to Twilio, please tell us why you\'re calling')
    #response.append(gather)
    response.say('Please leave a message at the beep.\nPress the star key when finished.')
    response.record(transcribe=True, transcribe_callback='http://127.0.0.1:5000/completed', finish_on_key='*')

    print(response)
    response.say(str(response))
    return(str(response))

@app.route("/completed", methods=['GET', 'POST'])
def recordings():

    print()

if __name__ == "__main__":
    app.run()