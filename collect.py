##Edwin Gavis
##07-01-19 
##Exploratory scraping of congressional tweets 

import tweepy
import csv

TARGET = "@realDonaldTrump"

def get_tweets(api, user):
	tweets = []
	i = 0
	for t in tweepy.Cursor(api.user_timeline, 
					  screen_name = user, 
					  include_rts = True,  
					  wait_on_rate_limit=True).items():
		tweets.append([t.id_str, 
					   t.created_at,
					   t.retweet_count, 
					   t.text.encode("utf-8")])
		i += 1
		if i % 50 == 0:
			print("Collected " + str(i) + " tweets")
	print("Writing Tweets")
	write_tweets(tweets, user)

def write_tweets(t, user):
	with open('%s_tweets.csv' % user, 'w') as f:
		csvwriter = csv.writer(f)
		csvwriter.writerow(["id","created_at","retweets","text"])
		csvwriter.writerows(t)
	

def tweep_init():
	c_key, c_sec, a_key, a_sec = get_codes()
	auth = tweepy.OAuthHandler(c_key, c_sec)
	auth.set_access_token(a_key, a_sec)
	api = tweepy.API(auth)
	return api

def get_codes():
	with open("auth/con", 'r') as f:
		codes = f.readlines()
	with open("auth/access", 'r') as f:
		codes += f.readlines()
	codes = [c.strip() for c in codes]
	return codes
	
	
if __name__ == '__main__':
	print("Setting up API authorization")
	api = tweep_init()
	print("Getting tweets")
	get_tweets(api, TARGET)
