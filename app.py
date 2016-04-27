# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for
import get_twitter_data
import max_entropy_classifier,libsvm_classifier
import itertools
import dbcon
from datetime import datetime,timedelta,date
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
@app.route('/history/')
def history():
    result=dbcon.Searchresults.select().order_by(dbcon.Searchresults.search_id)
    items=[]
    j=1
    for i in result:
        an_item = dict(sno=j, date=i.time, keyword=i.search_keyword,  result=i.search_result, c=i.classifier_used)
        items.append(an_item)
        j=j+1
    return render_template('history.html',items=items)
# Define a route for the default URL, which loads the form
@app.route('/')
@app.route('/index')
def index():
    result=dbcon.Searchresults.select().order_by(dbcon.Searchresults.search_id.desc()).limit(10)
    items=[]
    j=1
    for i in result:
        an_item = dict(sno=j, date=i.time, keyword=i.search_keyword,  result=i.search_result, c=i.classifier_used)
        items.append(an_item)
        j=j+1
    if not items:
        print "no items"
        return render_template('form_submit.html',noelement=True)
    else:
        print "items"
        return render_template('form_submit.html',items=items)
        

def get_time(f):
    if f == 'today':
        i = datetime.now()
        return i.strftime('%Y/%m/%d')
    else:
        result=date.today() - timedelta(days=7)
        final= result.strftime('%Y/%m/%d') +" - "+datetime.now().strftime('%Y/%m/%d')
        return final


@app.route('/submit/', methods=['POST'])
def submit():
    try:
        keyword=request.form['yourname']
        time=request.form['options']
        twitterData = get_twitter_data.TwitterData()
        tweets = twitterData.getTwitterData(keyword, time)
        classifier = request.form['c']
        if classifier=="maxent":
            print "Maxent chosen"
            trainingDataFile = 'data/training_neatfile.csv'
            classifierDumpFile = 'data/maxent_trained_model.pickle'
            trainingRequired = 0
            maxent = max_entropy_classifier.MaxEntClassifier(tweets, keyword, time, \
                                      trainingDataFile, classifierDumpFile, trainingRequired)
            maxent.classify()
            val,val2,time,pos_count,neg_count,neut_count=maxent.print_value()
            pos_tweet,neg_tweet,neut_tweet=process(val,val2)
            print "maxent finished"
        else:
            trainingDataFile = 'data/training_neatfile.csv'                
            classifierDumpFile = 'data/svm_trained_model.pickle'
            trainingRequired = 0
            sc = libsvm_classifier.SVMClassifier(tweets, keyword, time, \
                                          trainingDataFile, classifierDumpFile, trainingRequired)
            sc.classify()
            print "classified"
            val,val2,time,pos_count,neg_count,neut_count=sc.print_value()
            pos_tweet,neg_tweet,neut_tweet=process(val,val2)
        res=str(pos_count)+" "+str(neut_count)+" "+str(neg_count)
        count = dbcon.Searchresults.select().count()
        if time == 'today':
            dbcon.Searchresults.create(time = get_time('today'),search_id=count+1,search_keyword=keyword,search_result=res,classifier_used=str(classifier))
            return render_template('form_action.html', name=keyword, option=get_time(time), pos_count=pos_count, neg_count=neg_count, neut_count=neut_count, pos_tweet=pos_tweet, neg_tweet=neg_tweet, neut_tweet=neut_tweet)
        elif time == 'lastweek':
            dbcon.Searchresults.create(time = get_time('week'),search_id=count+1,search_keyword=keyword,search_result=res,classifier_used=str(classifier))
            return render_template('form_action_weekly.html', name=keyword, option=get_time(time), pos_count=pos_count, neg_count=neg_count, neut_count=neut_count, pos_tweet=pos_tweet, neg_tweet=neg_tweet, neut_tweet=neut_tweet)
        else:
        	return render_template('form_submit.html',sorry="T")
    except:
        return render_template('form_submit.html',sorry="Y")
# Run the app :)
if __name__ == '__main__':
	app.jinja_env.cache = {}
	app.run(host="0.0.0.0",debug=True,threaded=True,port=5000)


