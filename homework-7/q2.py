from naive_bayes import naivebayes

import pandas as pd
import re
import math
import os     

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

# Function to test the classifier with data from a folder
def test_classifier(classifier, folder, category):
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r', encoding='utf-8') as f:
            text = f.read()
            predicted = classifier.classify(text, category)
            results.append((filename, category, predicted))

# Function to train classifier with data from a folder
def train_classifier(classifier, folder, category):
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r', encoding='utf-8') as f:
            text = f.read()
            classifier.train(text, category)

# Initialize function to extract features (words) from a document
nb = naivebayes(getwords)
nb.setdb('classifier.db')

# Train the classifier with the training dataset
train_classifier(nb, 'emails_dataset/training/on_topic', 'on_topic')
train_classifier(nb, 'emails_dataset/training/off_topic', 'off_topic')

# Results storage for testing phase
results = []

# Test the classifier with the testing dataset
test_classifier(nb, 'emails_dataset/testing/on_topic', 'on_topic')
test_classifier(nb, 'emails_dataset/testing/off_topic', 'off_topic')

# Convert results to a DataFrame and calculate accuracy
df = pd.DataFrame(results, columns=['File Name', 'Actual', 'Predicted'])
df['Correct'] = df['Actual'] == df['Predicted']

# Display and save the results
print(df)
df.to_csv('classification_results.csv', index=False)