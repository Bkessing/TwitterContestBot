# Twitter Contest Bot

Searches Twitter for Retweet Contests and will retweet, follow, and like the tweet accordingly.

## Disclamer

This bot is written purely for educational purposes. I hold no liability for what you do with this bot or what happens to you by this bot. Abusing this bot can get you banned from Twitter. Please refer to Twitter`s proper usage documentation. 

## License 

Feel free to fork this repository as long as it links back to the original. Please do not sell this script. 

## Prerequisites 

* Python 3.7
* Tweepy
* Emoji
* Twitter developer account

## Setup

Open and edit `Config.json` and use your own personal Twitter API credentials.

Make sure your Twitter settings allow direct messages for anyone.

## Configuration

* `search-query`: String that API with search on Twitter with.
* `follow-keywords`: If any of these words are in the Tweet, the script will follow the author.
* `like-keywords`: If any of these words are in the Tweet, the script will like or favorite the Tweet.
* `whitelist-tweets`: Must include one of these words to be Retweeted. 
* `blacklist-tweets`: If any of these words are in a tweet, the tweet will be skipped
* `blacklist-names`: If the author is in this list the tweet will be skipped. 
* `tweet-number`: Number of tweets to look at in a single search.
* `wait-time`: Time in seconds the script waits betweens searches.
* `max-followers`: Max number of followers you have until script unfollows users.
* `followers-to-remove`: Number of followers to remove once max-followers is reached.
* `regex-to-replace`: Regular expression string to remove from each tweet. 
* `consumer-key`: Your consumer key.
* `consumer-secret`: Your consumer secret.
* `access-token-key`: Your access token key.
* `access-token-secret`: Your access token secret.

## Installation 

* In Command Prompt run: `pip install Tweepy` and `pip install emoji`
* Open `Config.json` and update credentials
* Run `TwitterBot.py`

