# Angelhack x IBM: Call For Code Challenge 2019

EVA is a Cognitive Robo-Caller Service that automates the process of responding to 995 emergency calls. Using Machine Learning and Artificial Intelligence, EVA can automatically answer emergency calls, record a victim’s particulars, provide them with assistance and notify first responders of their location for rescue response.

Going beyond the collection of information from call centers, EVA also scapes social media platforms such as Twitter to collect information on disasters. With the emergence of the social media ecosystem, a vast amount of data is available on the internet but is not harnessed upon. EVA scrapes the internet for information, and highlights the top results to support emergency response.

Our solution not only solves the problem of the scalability of call centers during disasters, it takes into the next step of information consolidation on a dashboard. Information recorded from calls (Refer to - Section 2.1),  information scraped from social media sites  (Refer to - Section 2.2) and X are displayed onto a dashboard that allows for the civil defence forces of nations and emergency response teams to make decisions. 


### Create virtual environment

    $ conda create -n myenv python=3.7
    $ conda activate myenv
    
### Install Dependencies:

    $ pip install -r requirements.txt

### Run Flask App:

    $ python server.py
    
### Run Angular Dashboard:

    $ cd paper-dashboard-angular-master
    $ npm i
    $ npm start
    
### Set Up Ngroc (Re-run if expired)

    $ cd <directory-that-contains-ngroc>
    $ ./ngrok http 5000
    
### Other configurations

    1) Add Ngroc URL to Twilio Add-On Apps - https://www.twilio.com/console/add-ons
    2) Add new IBM API Keys by creating resources - https://cloud.ibm.com/catalog?search=label:lite&category=ai
    3) Twilio-Flask Tutorial: https://www.twilio.com/docs/voice/tutorials/how-to-respond-to-incoming-phone-calls-python
    4) Twilio-Flask Tutorial2: https://www.twilio.com/docs/voice/tutorials/how-to-record-phone-calls-python
