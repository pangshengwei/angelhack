# Angelhack x IBM: Call For Code Challenge 2019

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
    
### Other imporant things to configure 

    1) Add Ngroc URL to Twilio Add-On Apps - <https://www.twilio.com/console/add-ons>
    2) Add new IBM API Keys by creating resources - <https://cloud.ibm.com/catalog?search=label:lite&category=ai>
