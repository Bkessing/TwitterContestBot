import tweepy
import time
import logging
import sys
import re
import queue
import json
import emoji
import time
import os
logging.basicConfig(level=logging.INFO)

# Variables for logging
total_retweet = 0
total_blacklisted_names = 0
total_blacklisted_tweets = 0
total_like = 0
total_follow = 0

# Loading Configuration file
with open('Config.json') as data_file:    
    data = json.load(data_file)

# Putting data from configuration file into variables
consumer_key = data["consumer-key"]
consumer_secret = data["consumer-secret"]
access_token = data["access-token-key"]
access_token_secret = data["access-token-secret"]
search = data["search-query"]
follow_keywords = data["follow-keywords"]
like_keywords = data["like-keywords"]
whitelist_tweets = data["whitelist-tweets"]
blacklist_tweets = data["blacklist-tweets"]
blacklist_names = data["blacklist-names"]
tweet_number = data["tweet-number"]
wait_time = data["wait-time"]
max_followers = data["max-followers"]
followers_to_remove = data["followers-to-remove"]
regex_to_replace = data["regex-to-replace"]


# Twitter auth
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

# Used to translate strings with non uniform characters
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)



# Removes non need characters from tweet
def clean_tweet(tweet):
    allchars = [str for str in tweet]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_tweet = ' '.join([str for str in tweet.split() if not any(i in str for i in emoji_list)])
    clean_tweet = re.sub(regex_to_replace,"",clean_tweet)
    return clean_tweet

# unfollows friends or followers
def delete_friends():
    q = queue.Queue()
    following = api.friends_ids()
    following.reverse()
    for follower in following:
        q.put(follower)
    for i in range(0,followers_to_remove):
        api.destroy_friendship(q.get())
    print("Last 1000 friends deleted")

# Creates the log file
def createLogFile():
    local_time = time.asctime( time.local_time(time.time()) )
    local_time = local_time.replace(" ","_")
    local_time = local_time.replace(":","_")
    local_time = local_time.replace("__","_")
    log_name = "logs\log_" + local_time+".json"
    with open(log_name,'w',encoding='utf-8') as f:
        f.close()
    return log_name

# Updates the log file
def updateLogFile(log_name):
    log = {}
    log['log'] = []
    log['log'].append({
        'retweets': total_retweet,
        'blacklisted-names': total_blacklisted_names,
        'blackListed-tweets': total_blacklisted_tweets,
        'liked': total_like
    })
    with open(log_name,'w',encoding='utf-8') as f:
        json.dump(log,f, ensure_ascii=False, indent=4)
        f.close()
    
# Returns true if the tweet contains a word in the blacklisted array
def isBlacklisted(tweet_array):
    for elem in blacklist_tweets:
        if elem in tweet_array:
            global total_blacklisted_tweets
            total_blacklisted_tweets += 1
            return True
    return False
    
# Returns true if the tweet contains a word in the whitelisted array
def isWhitelisted(tweet_array):
    for elem in whitelist_tweets:
        if elem in tweet_array:
            return True
    return False

# Returns true if the author of the tweet is in the blacklisted name array
def isBlacklistedName(tweet):
    for elem in blacklist_names:
        if elem in tweet.author.name:
            global total_blacklisted_names
            total_blacklisted_names += 1
            return True
    return False
    
# Main loop to search and retweet tweets
def twitterBot():
    log_name = createLogFile()
    while(True):
        retweet_count = 0
        try:
            for tweet in tweepy.Cursor(api.search,search, result_type= "latest",count = 100 ).items(tweet_number):
                    
                cleaned_tweet = clean_tweet(tweet.text)
                tweet_trray = cleaned_tweet.split()
                tweet_array = [item.lower() for item in tweet_array]

                if isBlacklistedName(tweet):
                    continue

                if not isBlacklisted(tweet_array) and isWhitelisted(tweet_array):
                    for elem in likeKeywords:
                        if elem in tweet_array:
                            global totalLike
                            tweet.favorite()
                            total_like += 1
                            break
                    for elem in followKeywords:
                        if elem in tweet_array:
                            global total_follow
                            api.create_friendship(tweet.author.screen_name)
                            total_follow += 1
                            break
                    tweet.retweet()
                    retweet_count += 1
                else:
                    continue
        except tweepy.TweepError as e:
            if(e.api_code == 185):
                print("Over usage sleeping for 30 min")
                time.sleep(1800)
            elif(e.api_code == 161):
                print("Can't follow")
            elif(e.api_code != 327 and e.api_code != 139):
               print(e)
        if retweet_count > 0:
            print(" Retweet: " + str(retweet_count), flush = True)
            global total_retweet
            total_retweet += retweet_count
        if(len(api.friends_ids()) >= max_followers):
            delete_friends()
        updateLogFile(log_name)
        time.sleep(wait_time)
           

twitterBot()
