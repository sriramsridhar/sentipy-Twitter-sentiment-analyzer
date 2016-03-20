import peewee as pw

myDB = pw.MySQLDatabase("sentipy", host="localhost", user="root", passwd="svss1995")


class MySQLModel(pw.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = myDB


class Searchresults(MySQLModel):
    time = pw.TextField()
    search_id=pw.IntegerField()
    search_keyword = pw.TextField()
    search_result = pw.CharField()
    classifier_used = pw.TextField()
    
    class Meta:
        order_by = ('search_id',)

# when you're ready to start querying, remember to connect
myDB.connect()
myDB.create_tables([Searchresults], safe=True)
