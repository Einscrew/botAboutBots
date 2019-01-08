import json, requests, tweepy, sys, time, inflect
from fdict import sfdict

p = inflect.engine()
INTERVAL = 60 * 1

RETWEET  = True

cache = sfdict(filename = 'history.db')
def erase():
	api = authenticate()

	for id in cache.values():
		try:
			api.destroy_status(id)
			print('Destroyed: ',id)
			time.sleep(INTERVAL)
		except tweepy.error.TweepError as e:
		 	print(e, id)
		

def makeFile():
	with open('sentences.txt','w') as f:
		for i in range(1,20):
			f.write('This is my '+str(p.ordinal(i))+' tweet\n')

def exit():
	print('Force Terminating...')
	cache.sync()
	cache.close()
	print('Done...')
	sys.exit(0)

def postTweet(api, tweet):
	try:
		print('Posting', tweet)
		id = api.update_status(status=tweet).id
		print('>>>>>>>',id)
		print(id, tweet, 'sleepling '+str(INTERVAL)+'s')
		if id:
			cache[tweet] = id
	except tweepy.error.TweepError as e:
		print('Erasing to repost')
		api.destroy_status(cache[tweet])
		id = api.update_status(status=tweet).id
		print('done',id, tweet, 'sleepling '+str(INTERVAL)+'s')
		if id:
			cache[tweet] = id

def main(content = 'sentences.txt'):
	api = authenticate()

	with open(content,'r') as f:
		content = f.read().split('\n')

	for tweet in content:
		try:
			postTweet(api, tweet)
			time.sleep(INTERVAL)
		except KeyboardInterrupt:
			exit()


def authenticate():
	with open('keys.json','r') as f: 
		keys=json.load(f)
	
	auth = tweepy.OAuthHandler(keys['consumer_key'],keys['consumer_secret'])
	auth.set_access_token(keys['token'],keys['token_secret'])
	api = tweepy.API(auth)
	return api

	

if __name__ == '__main__':
	print('Started...')
	main()
	print('Terminating...')