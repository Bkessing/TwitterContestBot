import tweepy
import time
import logging
logging.basicConfig(level=logging.INFO)

consumerKey = ""
consumerSecret = ""
accessToken = ""
accessTokenSecret = ""

auth = tweepy.OAuthHandler(consumerKey,consumerSecret)
auth.set_access_token(accessToken,accessTokenSecret)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


search = "giveaway OR #giveaway OR sweepstakes OR #sweepstakes -filter:retweets -filter:replies"
badTweetFilter = ["tag","reply","comment","share","bot","sub","subscribe","dm","click","#sugardaddy","#sugarbabe"
                  , "vbucks", "roblox","fortnite","ipx6","au","taotronics","instagram","#sugarbaby","sugardaddys","sugar","baby","pinned","#sugarmummy","cashapp"]
goodTweetFilter = ["retweet","#retweet","rt2win","rt","rt!","-rt","#rt","retweet!"]
nameFilter = ["spotting","Spotting","Spotter","spotter","B0t","Aek_bot","i love","PaperLeaf.ca"]


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
                tweetArray = tweet.text.split()
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
                        tweet.author.follow()
                    tweet.retweet()
                    retweetCount = retweetCount + 1
                        
                else:
                    continue
            except tweepy.TweepError as e:
                if(e.api_code == 185):
                    print("Over usage sleeping for 30 min")
                    time.sleep(1800)
                elif(e.api_code == 161):
                    print("Unable to follow more people at this time, sleeping for 1 hour")
                    time.sleep(3600)
                elif(e.api_code != 327 and e.api_code != 139):
                   print(e.reason)
        print(" Retweet: " + str(retweetCount), flush = True)
        time.sleep(300)
           

 
twitterBot()