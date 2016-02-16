import get_twitter_data
import max_entropy_classifier
import itertools

def submit(keyword,time):
    print "Analysing "+keyword+ " for "+time+" : \n"
    twitterData = get_twitter_data.TwitterData()
    tweets = twitterData.getTwitterData(keyword, time)
    print "The collected tweets are : \n"
    trainingDataFile = 'data/training_neatfile.csv'
    classifierDumpFile = 'data/maxent_trained_model.pickle'
    trainingRequired = 0
    maxent = max_entropy_classifier.MaxEntClassifier(tweets, keyword, time, \
                              trainingDataFile, classifierDumpFile, trainingRequired)
    maxent.classify()
    val,val2,time,pos_count,neg_count,neut_count=maxent.print_value()
    items=len(val2)-1
    for i in range(0,items):
        print val[i]+ " : " + val2[i]+ "\n"
    print "The positive count be : "+str(pos_count)
    print "The negative count be : "+str(neg_count)
    print "The neutral count be : "+str(neut_count)
    return 0


if __name__ == '__main__':
    keyword=raw_input("Please enter the keyword : ")
    timeline=raw_input("Please enter the time period (today/lastweek) : ")
    submit(keyword,timeline)



