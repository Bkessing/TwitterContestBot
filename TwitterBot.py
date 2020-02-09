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

totalRetweet = 0
totalBlacklistedNames = 0
totalBlacklistedTweets = 0
totalLike = 0
totalFollow = 0

with open('Config.json') as data_file:    
    data = json.load(data_file)

consumerKey = data["consumer-key"]
consumerSecret = data["consumer-secret"]
accessToken = data["access-token-key"]
accessTokenSecret = data["access-token-secret"]
search = data["search-query"]
followKeywords = data["follow-keywords"]
likeKeywords = data["like-keywords"]
whitelistTweets = data["whitelist-tweets"]
blacklistTweets = data["blacklist-tweets"]
blacklistNames = data["blacklist-names"]
tweetNumber = data["tweet-number"]
waitTime = data["wait-time"]
maxFollowers = data["max-followers"]
followersToRemove = data["followers-to-remove"]
regexToReplace = data["regex-to-replace"]


auth = tweepy.OAuthHandler(consumerKey,consumerSecret)
auth.set_access_token(accessToken,accessTokenSecret)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)




def clean_tweet(tweet):
    allchars = [str for str in tweet]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    cleanTweet = ' '.join([str for str in tweet.split() if not any(i in str for i in emoji_list)])
    cleanTweet = re.sub(regexToReplace,"",cleanTweet)
    return cleanTweet

def delete_friends():
    q = queue.Queue()
    following = api.friends_ids()
    following.reverse()
    for follower in following:
        q.put(follower)
    for i in range(0,followersToRemove):
        api.destroy_friendship(q.get())
    print("Last 1000 friends deleted")

def createLogFile():
    localtime = time.asctime( time.localtime(time.time()) )
    localtime = localtime.replace(" ","_")
    localtime = localtime.replace(":","_")
    localtime = localtime.replace("__","_")
    logName = "logs\log_" + localtime+".json"
    with open(logName,'w',encoding='utf-8') as f:
        f.close()
    return logName

def updateLogFile(logName):
    log = {}
    log['log'] = []
    log['log'].append({
        'retweets': totalRetweet,
        'blacklistedNames': totalBlacklistedNames,
        'blackListedTweets': totalBlacklistedTweets,
        'liked': totalLike
    })
    with open(logName,'w',encoding='utf-8') as f:
        json.dump(log,f, ensure_ascii=False, indent=4)
        f.close()
    
    

def log(attribute,update):
    print(test)

def isBlacklisted(tweetArray):
    for elem in blacklistTweets:
        if elem in tweetArray:
            global totalBlacklistedTweets
            totalBlacklistedTweets += 1
            return True
    return False

def isWhitelisted(tweetArray):
    for elem in whitelistTweets:
        if elem in tweetArray:
            return True
    return False
def isBlacklistedName(tweet):
    for elem in blacklistNames:
        if elem in tweet.author.name:
            global totalBlacklistedNames
            totalBlacklistedNames += 1
            return True
    return False
    
def twitterBot():
    logName = createLogFile()
    while(True):
        retweetCount = 0
        for tweet in tweepy.Cursor(api.search,search, result_type= "latest",count = 100 ).items(1000):
            try:
                
                cleanedTweet = clean_tweet(tweet.text)
                tweetArray = cleanedTweet.split()
                tweetArray = [item.lower() for item in tweetArray]

                if isBlacklistedName(tweet):
                    continue

                if not isBlacklisted(tweetArray) and isWhitelisted(tweetArray):
                    for elem in likeKeywords:
                        if elem in tweetArray:
                            global totalLike
                            tweet.favorite()
                            totalLike += 1
                            break
                    for elem in followKeywords:
                        if elem in tweetArray:
                            global totalFollow
                            api.create_friendship(tweet.author.screen_name)
                            totalFollow += 1
                            break
                    tweet.retweet()
                    retweetCount = retweetCount + 1
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
        if retweetCount > 0:
            print(" Retweet: " + str(retweetCount), flush = True)
            global totalRetweet
            totalRetweet += retweetCount
        if(len(api.friends_ids()) >= maxFollowers):
            delete_friends()
        updateLogFile(logName)
        time.sleep(waitTime)
           

twitterBot()
