##Edwin Gavis
##07-01-19 
##Exploratory scraping of congressional tweets 

import tweepy
import csv

TARGET = ""

def get_tweets(api, user):
	'''
	tweets = api.user_timeline(screen_name = user,count=200)
	last = tweets[-1].id - 1
	n_added = len(tweets)
	while n_added:
		tweets += api.user_timeline(screen_name = user,count=200, max_id = last)
		n_added = len(tweets) - 
	'''
	s = tweepy.Cursor(api.user_timeline, screen_name = user, include_rts = True)
	tweets = []
	while True:
		try:
			t = c.next()
			tweets.append([t.id_str, t.created_at, t.text.encode("utf-8")])
		except tweepy.TweepError:
       		time.sleep(60 * 15)
        	continue
		except StopIteration:
			break 
	write_tweets(tweets, user)

def write_tweets(t, user):
	with open('%s_tweets.csv' % user, 'wb') as f:
		csvwriter = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(t)
	
def tweep_init():
	auth = tweepy.OAuthHandler(get_codes(consumer = True))
	auth.set_access_token(get_codes(consumer = False))
	api = tweepy.API(auth)
	return api

def get_codes(consumer):
	target = "auth/access"
	if consumer:
		target = "auth/con"
	with open(target, 'r') as f:
		codes = f.readlines()
		codes = [c.strip() for c in codes]
	return codes[0], codes[1]
	
if __name__ == '__main__':
	pass
