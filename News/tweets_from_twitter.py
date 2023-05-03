import datetime
import secret
from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import requests

# Your Twitter Bearer Token
bearer_token = secret.bearer_token

# Authenticate with the Twitter API
headers = {"Authorization": f"Bearer {bearer_token}"}

# The existing code for sentiment analysis, confidence_label, and get_importance_score functions
def confidence_label(confidence_score):
    if confidence_score >= 0.75:
        return "Very High"
    elif confidence_score >= 0.5:
        return "High"
    elif confidence_score >= 0.25:
        return "Medium"
    else:
        return "Low"

def get_importance_score(summary):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(summary)
    compound_score = sentiment_scores['compound']

    # Normalize the compound score to a 0-10 range
    importance_score = (compound_score + 1) * 5

    # Determine the sentiment label and confidence score based on the sentiment scores
    if compound_score > 0.05:
        sentiment_label = 'Bullish'
        confidence_score = sentiment_scores['pos']
    elif compound_score < -0.05:
        sentiment_label = 'Bearish'
        confidence_score = sentiment_scores['neg']
    else:
        sentiment_label = 'Neutral'
        confidence_score = sentiment_scores['neu']

    return importance_score, sentiment_label, confidence_score

def get_crypto_tweets_v2(crypto_name, from_date):
    query = f"{crypto_name} -is:retweet lang:en"
    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=100&tweet.fields=created_at&expansions=author_id&user.fields=username"

    response = requests.get(url, headers=headers)
    data = response.json()

    if 'data' not in data:
        print("Error: No data found in the API response")
        return []

    results = []

    # Iterate through tweets and extract information
    for tweet in data['data']:
        text = tweet['text']
        user_id = tweet['author_id']
        created_at = tweet['created_at']
        tweet_id = tweet['id']

        username = None
        for user in data['includes']['users']:
            if user['id'] == user_id:
                username = user['username']
                break

        tweet_url = f"https://twitter.com/{username}/status/{tweet_id}"

        importance, sentiment_label, confidence_score = get_importance_score(text)

        results.append({
            'text': text,
            'url': tweet_url,
            'importance': importance,
            'sentiment_label': sentiment_label,
            'confidence_score': confidence_score,
            'created_at': created_at,
            'user': username
        })

    return results

# Example usage
crypto_name = input("Enter the name of the crypto asset: ")

# Get the date from the user and convert it to a datetime object
from_date_str = input("Enter the start date for tweets (YYYY-MM-DD): ")
from_date = datetime.datetime.strptime(from_date_str, '%Y-%m-%d')

tweets = get_crypto_tweets_v2(crypto_name, from_date)

# Sort the tweets by importance in descending order
sorted_tweets = sorted(tweets, key=lambda x: x['importance'], reverse=True)

# Filter the top N most important tweets
N = 20
top_tweets = sorted_tweets[:N]

# Print the top N tweets in a cleaner format
for i, tweet in enumerate(top_tweets, start=1):
    print(f"Tweet {i}:")
    print(f"Text: {tweet['text']}")
    print(f"URL: {tweet['url']}")
    print(f"Importance: {tweet['importance']:.2f}")
    print(f"Sentiment: {tweet['sentiment_label']}")
    print(f"Confidence: {confidence_label(tweet['confidence_score'])}")
    print(f"Created At: {tweet['created_at']}")
    print(f"User: {tweet['user']}")
    print("\n")

print('-- Done')

# Generate the DataFrame
df = pd.DataFrame(top_tweets)
if 'text' in df.columns:
    df['Text'] = df['text']
else:
    print("Error: 'text' column not found in DataFrame")

if 'created_at' in df.columns:
    df['Created At'] = df['created_at'].apply(lambda x: x.strftime('%Y-%m-%d'))
if 'confidence_score' in df.columns:
    df['Confidence'] = df['confidence_score'].apply(confidence_label)
if 'user' in df.columns:
    df['User'] = df['user']
df = df[['Text', 'Created At', 'importance', 'sentiment_label', 'Confidence', 'User']]
df.columns = ['Text', 'Date', 'Importance', 'Sentiment', 'Confidence', 'User']

# Save the DataFrame to a CSV file
output_file = "crypto_tweets.csv"
df.to_csv(output_file, index=False)

print(f"Top {N} tweets saved to {output_file}")
