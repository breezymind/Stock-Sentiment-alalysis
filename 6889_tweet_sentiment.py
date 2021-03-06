import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import time

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'oDKDLROopWOudtZmVCz6bX4r4'
        consumer_secret = 'a4bXwdppENH2UNuHIRk1swa26iRqlCnxGegM4cVyvFspIIpFr4'
        access_token = '848214270726856706-vNX1CHLJ8qVWNzaMSoYTk1USja1fJFE'
        access_token_secret = 'ArWd0bcMAeXa7aDKGJ0UZ09f2RONLlxXpHJKxU1x8EMXf'

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

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) \
                                    |(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
        
        c = tweepy.Cursor(self.api.search, q=query).items(count)
        while True:
            try:
                tweet = c.next()
                # call twitter api to fetch tweets and parse tweets one by one
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
                
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                # saving the created time of tweet
                parsed_tweet['time'] = tweet.created_at

                # appending parsed tweet to tweets list
                tweets.append(parsed_tweet)
                
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
                
                # return parsed tweets
                if len(tweets) == count:
                    return tweets
            
            except tweepy.TweepError as e:
                print("Error : " + str(e))
                print("please wait for 15mins...")
                time.sleep(60 * 15)
                continue
                
def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    search_input = raw_input("Please input the content you want to search: ")
    cnt = raw_input("Please input the quantity of the tweets you want to search: ")
    tweets = api.get_tweets(query = search_input, count = int(cnt))

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} % ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))

    print(len(tweets))
    print(len(ptweets))
    print(len(ntweets))
    # print positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:-1]:
        print(tweet['text'])
        print(tweet['time'])
        print('-------------------')

    # print negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:-1]:
        print(tweet['text'])
        print(tweet['time'])
        print('-------------------')

if __name__ == "__main__":
    # calling main function
    main()
