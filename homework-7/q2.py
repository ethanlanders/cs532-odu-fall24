import sqlite3 as sqlite
import pandas as pd
import re
import math
import os

class classifier:
  def __init__(self,getfeatures,filename=None):
    # Counts of feature/category combinations
    self.fc={}
    # Counts of documents in each category
    self.cc={}
    self.getfeatures=getfeatures
    
  def setdb(self,dbfile):
    self.con=sqlite.connect(dbfile)    
    self.con.execute('create table if not exists fc(feature,category,count)')
    self.con.execute('create table if not exists cc(category,count)')

  def incf(self,f,cat):
    count=self.fcount(f,cat)
    if count==0:
      self.con.execute("insert into fc values ('%s','%s',1)" 
                       % (f,cat))
    else:
      self.con.execute(
        "update fc set count=%d where feature='%s' and category='%s'" 
        % (count+1,f,cat)) 
  
  def fcount(self,f,cat):
    res=self.con.execute(
      'select count from fc where feature="%s" and category="%s"'
      %(f,cat)).fetchone()
    if res==None: return 0
    else: return float(res[0])

  def incc(self,cat):
    count=self.catcount(cat)
    if count==0:
      self.con.execute("insert into cc values ('%s',1)" % (cat))
    else:
      self.con.execute("update cc set count=%d where category='%s'" 
                       % (count+1,cat))    

  def catcount(self,cat):
    res=self.con.execute('select count from cc where category="%s"'
                         %(cat)).fetchone()
    if res==None: return 0
    else: return float(res[0])

  def categories(self):
    cur=self.con.execute('select category from cc');
    return [d[0] for d in cur]

  def totalcount(self):
    res=self.con.execute('select sum(count) from cc').fetchone();
    if res==None: return 0
    return res[0]

  def train(self,item,cat):
    features=self.getfeatures(item)
    # Increment the count for every feature with this category
    for f in features:
      self.incf(f,cat)

    # Increment the count for this category
    self.incc(cat)
    self.con.commit()

  def fprob(self,f,cat):
    if self.catcount(cat)==0: return 0

    # The total number of times this feature appeared in this 
    # category divided by the total number of items in this category
    return self.fcount(f,cat)/self.catcount(cat)

  def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
    # Calculate current probability
    basicprob=prf(f,cat)

    # Count the number of times this feature has appeared in
    # all categories
    totals=sum([self.fcount(f,c) for c in self.categories()])

    # Calculate the weighted average
    bp=((weight*ap)+(totals*basicprob))/(weight+totals)
    return bp

     


class naivebayes(classifier):   # change for basic_classifier

  def __init__(self,getfeatures):   
    classifier.__init__(self,getfeatures)  # change for basic_classifier
    self.thresholds={}
  
  def docprob(self,item,cat):
    features=self.getfeatures(item)   

    # Multiply the probabilities of all the features together
    p=1
    for f in features: p*=self.weightedprob(f,cat,self.fprob)
    return p

  def prob(self,item,cat):
    catprob=self.catcount(cat)/self.totalcount()
    docprob=self.docprob(item,cat)
    return docprob*catprob
  
  def setthreshold(self,cat,t):
    self.thresholds[cat]=t
    
  def getthreshold(self,cat):
    if cat not in self.thresholds: return 1.0
    return self.thresholds[cat]
  
  def classify(self,item,default=None):
    probs={}
    # Find the category with the highest probability
    max=0.0
    for cat in self.categories():
      probs[cat]=self.prob(item,cat)
      if probs[cat]>max: 
        max=probs[cat]
        best=cat

    # Make sure the probability exceeds threshold*next best
    for cat in probs:
      if cat==best: continue
      if probs[cat]*self.getthreshold(best)>probs[best]: return default
    return best
     

# Helper function to extract features (words) from a document
def getwords(doc):
    splitter=re.compile('\W+')  # different than book
    #print (doc)
    # Split the words by non-alpha characters
    words=[s.lower() for s in splitter.split(doc) 
          if len(s)>2 and len(s)<20]
  
    # Return the unique set of words only
    uniq_words = dict([(w,1) for w in words])

    return uniq_words

# Initialize function to extract features (words) from a document
nb = naivebayes(getwords)
nb.setdb('classifier.db')

# Function to train classifier with data from a folder
def train_classifier(classifier, folder, category):
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r', encoding='utf-8') as f:
            text = f.read()
            classifier.train(text, category)

# Train the classifier with the training dataset
train_classifier(nb, 'emails_dataset/training/on_topic', 'on_topic')
train_classifier(nb, 'emails_dataset/training/off_topic', 'off_topic')

# Results storage for testing phase
results = []

# Function to test the classifier with data from a folder
def test_classifier(classifier, folder, category):
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r', encoding='utf-8') as f:
            text = f.read()
            predicted = classifier.classify(text, category)
            results.append((filename, category, predicted))

# Test the classifier with the testing dataset
test_classifier(nb, 'emails_dataset/testing/on_topic', 'on_topic')
test_classifier(nb, 'emails_dataset/testing/off_topic', 'off_topic')

# Convert results to a DataFrame and calculate accuracy
df = pd.DataFrame(results, columns=['File Name', 'Actual', 'Predicted'])
df['Correct'] = df['Actual'] == df['Predicted']

# Display and save the results
print(df)
df.to_csv('classification_results.csv', index=False)