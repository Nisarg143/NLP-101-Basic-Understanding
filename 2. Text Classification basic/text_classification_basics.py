# -*- coding: utf-8 -*-
"""Text Classification Basics.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XX-7IBXGq6gS5Rup1sm-gqmUiVyFTNo_
"""

# connecting to google drive for dataset and other files

from google.colab import drive
drive.mount('/content/gdrive')

# kaggle data: https://www.kaggle.com/datasets/kingburrito666/shakespeare-plays

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics as mt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from PIL import Image

df = pd.read_csv("gdrive/My Drive/Colab Notebooks/Shakespeare_data.csv")
df.head()

del [df['Player'],df['Dataline'],df['PlayerLinenumber'],df['ActSceneLine']]
df.head()

df['Play'].value_counts()

requires = {'Hamlet':0,'Coriolanus':1,'Cymbeline':2,'Richard III':3,'Antony and Cleopatra':4,
            'King Lear':5,'Othello':6,'Troilus and Cressida':7,'A Winters Tale':8,'Henry VIII':9,

            'Henry V':10,'Henry VI Part 2':11,'Romeo and Juliet':12,'Henry IV':13,'Henry VI Part 3':14,
            'Alls well that ends well':15,'Measure for measure':16,'Loves Labours Lost':17,'Henry VI Part 1':18,'Richard II':19,

            'Merry Wives of Windsor':20,'As you like it':21,'Taming of the Shrew':22,'Merchant of Venice':23,'Julius Caesar':24,
            'King John':25,'Titus Andronicus':26,'Much Ado about nothing':27,'Timon of Athens':28,'Twelfth Night':29,

            'Pericles':30,'macbeth':31,'The Tempest':32,'Two Gentlemen of Verona':33,'A Midsummer nights dream':34,'A Comedy of Errors':35
            }
df = df[df['Play'].isin(requires)]
df.head()

df['Play'] = df['Play'].map(requires)
df.head()

df.sample(frac=1).reset_index(drop=True,inplace=True)
print(df)

stop_word=nltk.corpus.stopwords.words('english')
stop_word.extend([',','?','""',"''",'.','!', "'",'"',"'d","'ll",'[',']','--',':',';','///','$'])

plt.figure(figsize=(10,10))
drama = df[df['Play']==0]
drama = ' '.join(drama['PlayerLine'])
wordcloud = WordCloud(background_color='black',width=1000,height=800, max_words=75
                          ,relative_scaling=1,stopwords=stop_word).generate(drama)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Hamlet')
plt.show()

count = [len(df.loc[df['Play']==x]) for x in range(0,36)]
freq_series = pd.Series(count)

# Plot the figure.
plt.figure(figsize=(12, 8))
ax = freq_series.plot(kind='barh')
ax.set_title('Play-Count')
ax.set_xlabel('count')
ax.set_ylabel('Play')
ax.set_yticklabels(requires.keys())

rects = ax.patches

Play = np.array(df['Play'],dtype='int')
PlayerLine = np.array(df['PlayerLine'])

print(Play)
print(PlayerLine)

def stopwords_removal(tokens):
    stop_words = nltk.corpus.stopwords.words('english')
    stop_words.extend([',','?','""',"''",'.','!', "'",'"',"'d","'ll",'[',']','--',':',';','///','$'])
    filtered_tokens = [i for i in tokens if not i in stop_words]
    return filtered_tokens

def stemming(tokens):
    stemmer = nltk.stem.porter.PorterStemmer()
    stemmed_tokens = [stemmer.stem(i) for i in tokens]
    return stemmed_tokens

def pre_process(text):
    tokens = text.lower()
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    tokens = stopwords_removal(tokens)
    final = stemming(tokens)
    return final

X_train, X_test, Y_train, Y_test = train_test_split(PlayerLine, Play, test_size=0.20,shuffle=True)

vectorizer = CountVectorizer(max_features=15000,lowercase=True, analyzer=pre_process, binary=False)
representation = vectorizer.fit_transform(X_train)
# print(representation)

representation_df = pd.DataFrame(data = representation.toarray(), columns=sorted(vectorizer.vocabulary_.keys()))
print(representation_df)

print(representation.shape)
print(representation_df.shape)









clf= RandomForestClassifier()
clf.fit(representation,Y_train)

prediction=clf.predict(vectorizer.transform(X_test))

# evaluating the model using accuracy

print(mt.accuracy_score(Y_test,prediction,normalize=True))
print(mt.classification_report(Y_test,prediction))
print(mt.confusion_matrix(Y_test,prediction))





from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC

clf = OneVsRestClassifier(SVC())
clf.fit(representation,Y_train)

prediction=clf.predict(vectorizer.transform(X_test))

# evaluating the model using accuracy

print(mt.accuracy_score(Y_test,prediction,normalize=True))
print(mt.classification_report(Y_test,prediction))
print(mt.confusion_matrix(Y_test,prediction))





from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression

clf = OneVsRestClassifier(LogisticRegression())
clf.fit(representation,Y_train)

prediction=clf.predict(vectorizer.transform(X_test))

# evaluating the model using accuracy

print(mt.accuracy_score(Y_test,prediction,normalize=True))
print(mt.classification_report(Y_test,prediction))
print(mt.confusion_matrix(Y_test,prediction))





