import time
from flask import Flask ,request
from recommendation_system import get_recommendations, sentiment_selection
app = Flask(__name__)


@app.route('/recommend_from_text', methods=['POST'])
def recommend_from_text():
    req = request.get_json()
    sentiment = req['sentiment']
    user_input = req['user_input']
    print(sentiment)
    print(user_input)
    return get_recommendations(sentiment, user_input)

@app.route('/select_sentiment', methods=['POST'])
def select_sentiment():
    req = request.get_json()
    sentiment = req['sentiment']
    return sentiment_selection(sentiment)