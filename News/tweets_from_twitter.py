import tweepy
import secret
from nltk.sentiment import SentimentIntensityAnalyzer

# Replace these with your own Twitter API keys and tokens
consumer_key = secret.twitter_consumer_key
consumer_secret = secret.twitter_consumer_secret
access_token = secret.twitter_access_token
access_token_secret = secret.twitter_access_token_secret

# List of influential crypto Twitter users (replace with your own list)
crypto_influencers = [
    "VitalikButerin",
    "elonmusk",
    "aantonop",
    "naval",
    "brian_armstrong",
]

def get_influencer_tweets(usernames, count=10):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    sia = SentimentIntensityAnalyzer()

    tweets_data = []

    for username in usernames:
        tweets = api.user_timeline(screen_name=username, count=count, tweet_mode="extended", lang="en")

        for tweet in tweets:
            if not tweet.retweeted and 'RT @' not in tweet.full_text:
                sentiment_scores = sia.polarity_scores(tweet.full_text)
                compound_score = sentiment_scores['compound']
                importance_score = (compound_score + 1) * 5

                tweet_data = {
                    'username': username,
                    'text': tweet.full_text,
                    'likes': tweet.favorite_count,
                    'retweets': tweet.retweet_count,
                    'sentiment': compound_score,
                    'importance': importance_score,
                }

                tweets_data.append(tweet_data)

    return tweets_data

# Fetch the tweets from the crypto influencers
tweets_data = get_influencer_tweets(crypto_influencers)

# Sort the tweets based on the importance, likes, and retweets
sorted_tweets = sorted(tweets_data, key=lambda x: (x['importance'], x['likes'], x['retweets']), reverse=True)

# Print the most important tweets
print("\nMost important tweets:\n")
for i, tweet in enumerate(sorted_tweets[:10], start=1):
    print(f"{i}. @{tweet['username']} - {tweet['text']}")
    print(f"   Likes: {tweet['likes']} | Retweets: {tweet['retweets']} | Sentiment: {tweet['sentiment']} | Importance: {tweet['importance']:.2f}\n")
