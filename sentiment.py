from textblob import TextBlob


def analyze_sentiment(review):
    polarity = TextBlob(review).sentiment.polarity

    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment, polarity