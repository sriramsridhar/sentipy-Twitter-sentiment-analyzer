from Tkinter import *
import get_twitter_data
import max_entropy_classifier
import itertools
from ScrolledText import *
import time
from ttk import Frame, Button, Style

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
    return val,val2,time,pos_count,neg_count,neut_count


def btn():
    keyword = str(test2.get())
    timeline=str(v.get())
    textPad.delete(0.0,END)
    if timeline=="":
        textPad.insert(INSERT, "Please check the timeline to analyse")
        return True
    textPad.delete(0.0,END)
    if keyword=="":
        textPad.insert(INSERT, "Please enter the search term to analyse")
        return True
    val,val2,time,pos_count,neg_count,neut_count = submit(keyword,timeline)
    items=len(val2)-1
    key_text= "\nThe positive count be : "+str(pos_count)+"\nThe negative count be : "+str(neg_count)+"\nThe neutral count be : "+str(neut_count)+"\n"
    s="\nThe processed tweets are : \n"
    for i in range(0,items):
        s+=str(val[i].encode('ascii', 'ignore'))+ " : " + str(val2[i].encode('ascii', 'ignore'))+ "\n"    
    key_text+=s
    textPad.insert(INSERT,str(key_text))


def gen():
    textPad.delete(0.0,END)
    pass


root = Tk()
root.config(background="#3b5998")
root.title("sentipy")
root.geometry("800x550")
root.style = Style()
root.style.theme_use("default")

test2_label = Label(root, text="Enter keyword to analyse")
test2_label.config(bg='White', fg='Black')
test2_label.grid(row=1,column=1, padx=20,pady=20,sticky=W)
test2 = Entry(root)
test2.config(bg='White',fg='Black')
test2.grid(row=1,column=2,columnspan=2,padx=5,pady=5,sticky=W)
test_label = Label(root, text="Enter time period")
test_label.config(bg='White', fg='Black')
test_label.grid(row=2,column=1, padx=20,pady=20,sticky=W)
v=StringVar()
r1=Radiobutton(root, text="Today", variable=v, value=" today ",indicatoron = 0)
r1.config(bg='White', fg='Black')
r1.grid(row=2,column=2)
r2=Radiobutton(root, text="Lastweek", variable=v, value="lastweek",indicatoron = 0)
r2.config(bg='White', fg='Black')
r2.grid(row=3,column=2)


bn1 = Button(root, text="Analyse", command=btn)
# bn1.config(bg='White', fg='Black')
bn1.grid(row=4,column=1,padx=50,pady=20,sticky=W)

bn3 = Button(root, text="clear console", command=gen)
# bn3.config(bg='White', fg='Black')
bn3.grid(row=4,column=2,padx=50,pady=5,sticky=E)
textPad = ScrolledText(root, width=110, height=25,bg='White',fg='Black')
# textPad.config(,anchor=E,justify=LEFT)
textPad.grid(row=6,column=1,columnspan=3,padx=5,pady=10,sticky=W)
#,rowspan=4

root.mainloop()
