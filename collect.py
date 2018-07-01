##Edwin Gavis
##07-01-19 
##Exploratory scraping of congressional tweets 

import tweepy

auth = tweepy.OAuthHandler(get_codes(consumer = True))
auth.set_access_token(get_codes(consumer = False))

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
	print tweet.text
	


def get_codes(consumer):
	target = "auth/access"
	if consumer:
		target = "auth/con"
	with open(target, 'r') as f:
		codes = f.readlines()
		codes = [c.strip() for c in codes]
	return codes[0], codes[1]
