import time
from flask import Flask, render_template, request
app = Flask(__name__)
from recommendation_system import get_recommendations

@app.route('/')
def index():
    print('INDEX')
    return render_template(
        'index.html'
    )
    
    
@app.route('/time')
def get_current_time():
    return {'time': time.time()}


@app.route('/recommend/')
@app.route('/recommend/<string:user_input>')
def recommend(user_input = None, methods=["POST", "GET"]):
    print('RECOMMEND')
    sentiment = request.args.get('sentiment')
    user_input = request.args.get('input')
    print('request: ', sentiment)
    print('request: ', user_input)
    if(user_input != None):
        most_common_words, most_similar_words, most_common_bigrams, next_bigrams = get_recommendations(1, user_input)
    #return render_template('recommend.html', **locals())
    return render_template('recommend.html')





if __name__ == "__main__":
    app.run(debug=True)