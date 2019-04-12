# -*- coding: utf-8 -*-

#Loading dependencies
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
import mglearn
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from math import log, sqrt
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer


#Load the data
comments = pd.read_csv('comments_data.csv')
comments.head()
comments = comments.drop(columns=['id', 'url'])

#train-test split
totalComments = comments['comment'].shape[0]
trainIndex, testIndex = list(), list()
for i in range(comments.shape[0]):
    if np.random.uniform(0,1) <0.75:
        trainIndex += [i]
    else:
        testIndex += [i]
trainData = comments.loc[trainIndex]
testData = comments.loc[testIndex]

trainData.reset_index(inplace = True)
trainData.drop(['index'], axis = 1, inplace = True)

print("Word cloud------------------------------------------------------------")
#wordcloud for bot
bot_words = ' '.join(list(comments[comments['isBot'] == 1]['comment']))
bot_wc = WordCloud(width = 512, height = 512).generate(bot_words)
plt.figure(figsize = (10, 8), facecolor = 'k')
plt.imshow(bot_wc)
plt.axis('off')
plt.tight_layout(pad = 0)
plt.show()
#wordcloud for non-bot
bot_words = ' '.join(list(comments[comments['isBot'] == 0]['comment']))
bot_wc = WordCloud(width = 512, height = 512).generate(bot_words)
plt.figure(figsize = (10, 8), facecolor = 'k')
plt.imshow(bot_wc)
plt.axis('off')
plt.tight_layout(pad = 0)
plt.show()
print("Word cloud------------------------------------------------------------")
print(' ')

#Training the model
        
#Bag of words
print("Bag of words----------------------------------------------------------")
text_train = list(trainData.loc[:,'comment'])
vect = CountVectorizer().fit(text_train)
x_train = vect.transform(text_train)
print("x_train:\n{}".format(repr(x_train)))
y_train = list(trainData.loc[:,'isBot'])

feature_names = vect.get_feature_names()
print("Number of features: {}".format(len(feature_names)))
print("First 20 features:\n{}".format(feature_names[:20]))
print("Features 5000 to 5020:\n{}".format(feature_names[5000:5020]))
print("Every 1000th feature:\n{}".format(feature_names[::1000]))
print("Bag of words----------------------------------------------------------")
print(' ')

#logistic regression
print("Linear Regression-----------------------------------------------------")
scores = cross_val_score(LogisticRegression(), x_train, y_train, cv = 10)
print("Mean cross-validation accuracy: {:.5f}".format(np.mean(scores)))

#10-fold CV
param_grid = {'C': [0.001, 0.01, 0.1, 1, 10]}
grid = GridSearchCV(LogisticRegression(), param_grid, cv=10)
grid.fit(x_train, y_train)
print("Best scross-validation score: {}".format(grid.best_score_))
print("Best parameters: ", grid.best_params_)

text_test = list(testData.loc[:,'comment'])
x_test = vect.transform(text_test)
y_test = list(testData.loc[:,'isBot'])
print("Test score: {:.5f}".format(grid.score(x_test, y_test)))
print("Linear Regression-----------------------------------------------------")
print(' ')

#x_train with min_df -- exclude features when its frequency is less than 5
print("With min_df 5---------------------------------------------------------")
vect = CountVectorizer(min_df = 5).fit(text_train)
x_train = vect.transform(text_train)
print("x_train with min_df: {}".format(repr(x_train)))

feature_names = vect.get_feature_names()
print("Number of features: {}".format(len(feature_names)))
print("First 20 features:\n{}".format(feature_names[:20]))
print("Features 500 to 520:\n{}".format(feature_names[500:520]))
print("Every 100th feature:\n{}".format(feature_names[::100]))

param_grid = {'C': [0.001, 0.01, 0.1, 1, 10]}
grid = GridSearchCV(LogisticRegression(), param_grid, cv=10)
grid.fit(x_train, y_train)
print("Best scross-validation score: {}".format(grid.best_score_))
print("Best parameters: ", grid.best_params_)
x_test = vect.transform(text_test)
y_test = list(testData.loc[:,'isBot'])
print("Test score: {:.5f}".format(grid.score(x_test, y_test)))
print("With min_df 5---------------------------------------------------------")
print(' ')

#Stopwords
print("With stopwords--------------------------------------------------------")
print("Number of stop words: {}".format(len(ENGLISH_STOP_WORDS)))
#print("Every 10th stopword:\n{}".format(list(ENGLISH_STOP_WORDS)[::10]))
vect = CountVectorizer(min_df = 5, stop_words = "english").fit(text_train)
x_train = vect.transform(text_train)
print("x_train with stop words:\n{}".format(repr(x_train)))

grid = GridSearchCV(LogisticRegression(), param_grid, cv=10)
grid.fit(x_train, y_train)
print("Best ccross-validation score: {}".format(grid.best_score_))
x_test = vect.transform(text_test)
y_test = list(testData.loc[:,'isBot'])
print("Test score: {:.5f}".format(grid.score(x_test, y_test)))
print("With stopwords--------------------------------------------------------")
print(' ')

#Rescaling the data with tf-idf
print("With tf-ide-----------------------------------------------------------")
pip = make_pipeline(TfidfVectorizer(min_df=5),
                    LogisticRegression())
param_grid = {'logisticregression_C': [0.001, 0.01, 0.1, 1, 10]}
grid.fit(x_train, y_train)
print("Best cross-validation score: {:.2f}".format(grid.best_score_))
x_test = vect.transform(text_test)
y_test = list(testData.loc[:,'isBot'])
print("Test score: {:.5f}".format(grid.score(x_test, y_test)))
print("With tf-ide-----------------------------------------------------------")


def process_message(comment, lower_case = True, stem = True, stop_words = True, gram = 2):
    if lower_case:
        comment = comment.lower()
    words = word_tokenize(comment)
    words = [w for w in words if len(w) > 2]
    if gram > 1:
        w = []
        for i in range(len(words) - gram + 1):
            w += [''.join(words[i:i + gram])]
        return w
    if stop_words:
        sw = stopwords.words('english')
        words = [word for word in words if word not in sw]
    if stem:
        stemmer = PorterStemmer()
        words = [stemmer.stem(word) for word in words]
    return words 
