import tweepy
import time
import logging
import sys
import re
import queue
logging.basicConfig(level=logging.INFO)

consumerKey = ""
consumerSecret = ""
accessToken = ""
accessTokenSecret = ""

auth = tweepy.OAuthHandler(consumerKey,consumerSecret)
auth.set_access_token(accessToken,accessTokenSecret)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

search = "giveaway OR #giveaway OR sweepstakes OR #sweepstakes -filter:retweets -filter:replies"
badTweetFilter = ["tag","reply","comment","share","bot","sub","subscribe","dm","click","#sugardaddy","#sugarbabe"
                  , "vbucks", "roblox","fortnite","ipx6","au","taotronics","instagram","#sugarbaby","sugardaddys","sugar"
                  ,"baby","pinned","#sugarmummy","cashapp","text"]
goodTweetFilter = ["retweet","#retweet","rt2win","rt","rt!","-rt","#rt","retweet!"]
nameFilter = ["spotting","Spotting","Spotter","spotter","B0t","Aek_bot","i love","PaperLeaf.ca"]


def delete_friends():
    q = queue.Queue()
    following = api.friends_ids()
    following.reverse()
    for f in following:
        q.put(f)
    for i in range(0,1000):
        api.destroy_friendship(q.get_nowait())
    print("Last 100 friends deleted")
    
def twitterBot():
    while(True):
        retweetCount = 0
        for tweet in tweepy.Cursor(api.search,search, result_type= "latest",count = 100 ).items(1000):
            try:
                bot = False
                for elem in nameFilter:
                    if elem in tweet.author.name:
                        bot = True
                        break
                if bot:
                    continue
                text = tweet.text.translate(non_bmp_map)
                replacedText = re.sub("-|,|:|\ufffd|!","",text)
                tweetArray = replacedText.split()
                tweetArray = [item.lower() for item in tweetArray]
                badResult = False
                goodResult = False
                for elem in badTweetFilter:
                    if elem in tweetArray:
                        badResult = True
                        break
                for elem in goodTweetFilter:
                    if elem in tweetArray:
                        goodResult = True
                        break
                if not badResult and goodResult:
                    if "like" in tweetArray or "fav" in tweetArray or "favorite" in tweetArray or "#like" in tweetArray :
                        tweet.favorite()
                    if "follow" in tweetArray  or "#follow" in tweetArray or "following" in tweetArray:
                        api.create_friendship(tweet.author.screen_name)
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
                   print(e.reason)
        if retweetCount > 0:
            print(" Retweet: " + str(retweetCount), flush = True)
        if(len(api.friends_ids()) >= 5000):
            delete_friends()
        time.sleep(300)
           

twitterBot()
