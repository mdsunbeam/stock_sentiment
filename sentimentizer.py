from transformers import pipeline

def sentimentize(text):
    sentiment = pipeline("sentiment-analysis")
    result = sentiment(text)[0]
    return result
