import requests
import datetime
import secret
from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import ssl
import pandas as pd
import webbrowser



try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('vader_lexicon')

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

print('\n')

def get_crypto_news(crypto_name, api_key, from_date):
    base_url = "https://newsapi.org/v2/everything"
    headers = {
        "X-Api-Key": api_key
    }
    from_date_str = from_date.strftime('%Y-%m-%d')  # Convert the from_date to a string format
    params = {
        "q": crypto_name,
        "language": "en",
        "sortBy": "relevancy",
        "from": from_date_str
    }

    response = requests.get(base_url, headers=headers, params=params)
    news = response.json()

    if news.get('status') == 'error':
        print(f"Error: {news['message']}")
        return []

    results = []

    # Iterate through articles and extract information
    for article in news['articles']:
        title = article['title']
        url = article['url']
        description = article['description']
        published_at = article['publishedAt']

        importance, sentiment_label, confidence_score = get_importance_score(description)

        results.append({
            'title': title,
            'url': url,
            'summary': description,
            'importance': importance,
            'sentiment_label': sentiment_label,
            'confidence_score': confidence_score,
            'published_at': published_at
        })

    return results


# Example usage
api_key = secret.api_key
crypto_name = input("Enter the name of the crypto asset: ")

# Get the date from the user and convert it to a datetime object
from_date_str = input("Enter the start date for news articles (YYYY-MM-DD): ")
from_date = datetime.datetime.strptime(from_date_str, '%Y-%m-%d')

# Check if the provided date is within the allowed range (modify the date accordingly)
earliest_allowed_date = datetime.datetime(2023, 3, 23)
if from_date < earliest_allowed_date:
    print(f"Your current plan allows fetching news articles from {earliest_allowed_date.strftime('%Y-%m-%d')} onwards.")
    from_date = earliest_allowed_date

news = get_crypto_news(crypto_name, api_key, from_date)

# Sort the news articles by importance in descending order
sorted_news = sorted(news, key=lambda x: x['importance'], reverse=True)

# Filter the top N most important news articles
N = 20
top_news = sorted_news[:N]

print('\n')

# Print the top N news articles in a cleaner format
for i, article in enumerate(top_news, start=1):
    print(f"Article {i}:")
    print(f"Title: {article['title']}")
    print(f"URL: {article['url']}")
    print(f"Summary: {article['summary']}")
    print(f"Importance: {article['importance']:.2f}")
    print(f"Sentiment: {article['sentiment_label']}")
    print(f"Confidence: {confidence_label(article['confidence_score'])}")
    print(f"Published At: {article['published_at']}")
    print("\n")

print('-- Done')

# Generate the HTML output
output_file = "crypto_news.html"
df = pd.DataFrame(top_news)
df['Title'] = df.apply(lambda x: f'<a href="{x["url"]}">{x["title"]}</a>', axis=1)
df['Published At'] = df['published_at'].apply(lambda x: x.split('T')[0])
df['Confidence'] = df['confidence_score'].apply(confidence_label)
df['Source'] = df['url'].apply(lambda x: f'<a href="{x}">Link</a>')  # Change the name Location to Source
df['Summary'] = df.index.to_series().apply(lambda x: f'{df.loc[x, "summary"][:100]}... <a href="#" onclick="toggleSummary({x})">View More</a><span id="full-summary-{x}" style="display:none;">{df.loc[x, "summary"]}</span>')  # Add a "view more" button to view more info
df = df[['title', 'Published At', 'importance', 'sentiment_label', 'Confidence', 'Summary', 'Source']]
df.columns = ['Title', 'Date', 'Importance', 'Sentiment', 'Confidence', 'Summary', 'Source']

html = df.to_html(escape=False, index=False)
html = html.replace('<table border="1" class="dataframe">', '<table class="dataframe">')

# Add CSS for better table formatting
css = '''
<style>
    body { font-family: Arial, sans-serif; font-size: 10px; }
    .dataframe {
        border-collapse: collapse;
        width: 100%;
    }
    .dataframe th, .dataframe td {
        border: 1px solid #ddd;
        padding: 8px;
    }
    .dataframe th {
        padding-top: 12px;
        padding-bottom: 12px;
        text-align: left;
        background-color: #f2f2f2;
        color: black;
    }
    .dataframe tr:nth-child(even) { background-color: #f2f2f2; }
    .dataframe tr:hover { background-color: #ddd; }
</style>
'''

today = datetime.datetime.now().strftime('%Y-%m-%d')
title = f"<h1>Important News About {crypto_name} Crypto Asset (From {from_date_str} to {today})</h1>"

js = '''
<script>
    function toggleSummary(index) {
        var fullSummary = document.getElementById("full-summary-" + index);
        if (fullSummary.style.display === "none") {
            fullSummary.style.display = "inline";
        } else {
            fullSummary.style.display = "none";
        }
    }
</script>
'''

with open(output_file, 'w') as f:
    f.write(css + title + html + js)

print(f"Top {N} news articles saved to {output_file}")

# Open the HTML file automatically
webbrowser.open(output_file, new=2)


