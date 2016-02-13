# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for
import get_twitter_data
import max_entropy_classifier
import itertools
# Initialize the Flask application
app = Flask(__name__)
def process(val,val2):
    pos_tweet=[]
    neg_tweet=[]
    neut_tweet=[]
    items=len(val2)-1
    for i in range(0,items):
        if val2[i] == "neutral":
            neut_tweet.append(val[i])
        elif val2[i] == "positive":
            pos_tweet.append(val[i])
        elif val2[i] == "negative":
            neg_tweet.append(val[i])
    return pos_tweet,neg_tweet,neut_tweet

# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('form_submit.html')

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/submit/', methods=['POST'])
def submit():
    keyword=request.form['yourname']
    time=request.form['options']
    print time
    twitterData = get_twitter_data.TwitterData()
    tweets = twitterData.getTwitterData(keyword, time)
    trainingDataFile = 'data/training_neatfile.csv'
    classifierDumpFile = 'data/maxent_trained_model.pickle'
    trainingRequired = 0
    maxent = max_entropy_classifier.MaxEntClassifier(tweets, keyword, time, \
                              trainingDataFile, classifierDumpFile, trainingRequired)
    maxent.classify()
    val,val2,time,pos_count,neg_count,neut_count=maxent.print_value()
    pos_tweet,neg_tweet,neut_tweet=process(val,val2)
    if time == 'today':
    	return render_template('form_action.html', name=keyword, option=time, pos_count=pos_count, neg_count=neg_count, neut_count=neut_count, pos_tweet=pos_tweet, neg_tweet=neg_tweet, neut_tweet=neut_tweet)
    elif time == 'lastweek':
    	return render_template('form_action_weekly.html', name=keyword, option=time, pos_count=pos_count, neg_count=neg_count, neut_count=neut_count, pos_tweet=pos_tweet, neg_tweet=neg_tweet, neut_tweet=neut_tweet)
    else:
    	return render_template('form_submit.html',sorry="T")
# Run the app :)
if __name__ == '__main__':
	app.jinja_env.cache = {}
	app.run(debug=True)


