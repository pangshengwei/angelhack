import re 
import tweepy 
from tweepy import OAuthHandler 
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
nltk.download('stopwords')
from credentials import *

class TwitterClient(object): 
	''' 
	Generic Twitter Class for sentiment analysis. 
	'''

	def __init__(self):
		''' 
		Class constructor or initialization method. 
		'''
		# attempt authentication 
		try: 
			# create OAuthHandler object 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			# set access token and secret 
			self.auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed") 

	def get_tweets(self, query, count): 

		tweets = []

		fetched_tweets = self.api.search(q = "Empire State Building Fire", count = count)

		for tweet in fetched_tweets: 
			parsed_tweet = re.sub(r'RT @\S+|https?://\S+|\n', '', tweet.text)

			if tweet.retweet_count > 0: 
				if parsed_tweet not in tweets: 
					tweets.append(parsed_tweet)
			else: 
				tweets.append(parsed_tweet)

		return tweets 

def ReturnCorpus(search_query):
	api = TwitterClient()

	tweets = api.get_tweets(query = search_query, count = 10000)

	corpus = []
	for tweet in tweets: 
		corpus.extend(word_tokenize(tweet))
	stop_words = stopwords.words('english')
	corpus = [word.lower() for word in corpus if  word.isalpha()]
	corpus = [word for word in corpus if word not in stop_words]

	frequencies = Counter(corpus).most_common(10)
	words = [item[0] for item in frequencies]

	return words
