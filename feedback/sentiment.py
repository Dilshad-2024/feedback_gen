from transformers import pipeline


classifier = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

def analyze_sentiment(text):

    result = classifier(text)[0]

    result["label"] = result["label"].upper()

    return result
