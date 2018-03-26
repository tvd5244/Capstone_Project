import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
import operator
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.model_selection import cross_val_predict




df = pd.read_csv("train.csv", index_col="PersonID")
df.target = df.ClusterClassifier.astype('category')
df.head()




ITEMS = 15
clusters=["","Sports","Computer Nerds","Anime","Computer Science","Math","Theater","Sing and Dance","Music","Movies","Food"]
v = CountVectorizer(ngram_range=(1,3),max_features=ITEMS)


for i in range(1,len(clusters)):
    df_x = v.fit_transform(df[df.ClusterClassifier == i].Interests.values.astype('U'))
    print("\nTop",ITEMS,"Interests for",clusters[i],"People")
    n = 1
    for ingr in sorted(v.vocabulary_.items(), key=operator.itemgetter(1)):
        print(n,ingr[0])
        n += 1

ITEMS = 50
v = TfidfVectorizer(sublinear_tf=True, ngram_range=(1,3),max_features=ITEMS)
df_x = v.fit_transform(df.Interests.values.astype('U'))
idf = v.idf_

topInterests = pd.DataFrame({"Interest": v.get_feature_names(),"TfIdf":idf})
print("Top",ITEMS,"Interests")
topInterests.sort_values(by="TfIdf",ascending=False)

# Match the user with other users who were put in the same category

nltk.download('punkt') # Download the required nltk data files

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = []
    for item in tokens:
        stems.append(PorterStemmer().stem(item))
    #print(stems)
    return stems
    

ITEMS = 50
v = TfidfVectorizer(sublinear_tf=True, tokenizer=tokenize, stop_words='english', ngram_range=(1,3),max_features=ITEMS)
df_x = v.fit_transform(df.Interests.values.astype('U'))
idf = v.idf_

topInterests = pd.DataFrame({"Interest": v.get_feature_names(),"TfIdf":idf})
print("Top",ITEMS,"Interests")
topInterests.sort_values(by="TfIdf",ascending=False)

df = pd.read_csv("train.csv", index_col="PersonID")
df.clusterclassifier = df.ClusterClassifier.astype('category')

bestK = None
bestKMeanAcc = 0

v = CountVectorizer(max_features=100)
df_x = v.fit_transform(df.Interests.values.astype('U')).todense()

for k in [3,5,7]:    
    knn = KNeighborsClassifier(n_neighbors = k, weights='uniform',
                               algorithm="auto")
    scores = cross_val_score(knn, df_x, df.target, cv=10)

    print("For k =",k," mean accuracy accross folds =",scores.mean()," standard deviation across folds =",scores.std())
    if bestK == None or scores.mean() < bestKMeanAcc:
        bestK = k
        bestKMeanAcc = scores.mean()
        
print("Best k =", k,"with estimated accuracy of",scores.mean())


# Load Training Set
dfTrain = pd.read_csv("train.csv", index_col="PersonID")
trainY = dfTrain.ClusterClassifier.astype('category')

dfTrain = dfTrain.drop(["ClusterClassifier"],axis=1)
df = pd.concat([dfTrain,pd.read_csv("test.csv", index_col="PersonID")])

v = CountVectorizer(max_features=100)
df_x = v.fit_transform(df.Interests.values.astype('U')).todense()

trainX = df_x[:len(dfTrain)]
testX = df_x[len(dfTrain):]


knn = KNeighborsClassifier(n_neighbors=7, weights='uniform', algorithm="auto")
knn.fit(trainX,trainY)

predictions = knn.predict(testX)

submissions = pd.read_csv("sampleSubmission.csv", index_col="PersonID")
submissions.ClusterClassifier = predictions

submissions.to_csv("submission.csv")


# Load dataset
df = pd.read_csv("train.csv", index_col="PersonID")

# Shuffle rows in dataset 
df = df.sample(frac=1)


v = CountVectorizer(max_features=100)
df_x = v.fit_transform(df.Interests.values.astype('U')).todense()

knn = KNeighborsClassifier(n_neighbors=7, weights='uniform', algorithm="auto")
predictions = cross_val_predict(knn, df_x, df.ClusterClassifier, cv=10)


pd.crosstab(predictions,df.ClusterClassifier,rownames=['Predictions'],colnames=['Actual Values'])

ITEMS = 15
clusters=["","Sports","Computer Nerds","Anime","Computer Science","Math","Theater","Sing and Dance","Music","Movies","Food"]

dfTest = df[int(len(df.index)*0.8):]

for prediction in range(1,8):
    for actual in range(1,8):
        v = CountVectorizer(max_features=ITEMS)
        if np.sum(np.logical_and(predictions==prediction,df.ClusterClassifier==actual)) > 0:
            df_cell = v.fit_transform(df[np.logical_and(predictions==prediction,df.ClusterClassifier==actual)].Interests.values.astype('U')).todense()
            print("\nTop",ITEMS,"Interests for",clusters[actual],"classified as",clusters[prediction])
            n = 1
            for ingr in sorted(v.vocabulary_.items(), key=operator.itemgetter(1)):
                print(n,ingr[0])
                n += 1
