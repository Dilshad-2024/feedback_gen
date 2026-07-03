# from transformers import pipeline


# classifier = pipeline(
#     "sentiment-analysis",
#     model="cardiffnlp/twitter-roberta-base-sentiment-latest"
# )

# def analyze_sentiment(text):

#     result = classifier(text)[0]

#     result["label"] = result["label"].upper()

#     return result
from transformers import pipeline

classifier = None


def analyze_sentiment(text):
    global classifier

    if classifier is None:
        classifier = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )

    result = classifier(text)[0]
    result["label"] = result["label"].upper()

    return result