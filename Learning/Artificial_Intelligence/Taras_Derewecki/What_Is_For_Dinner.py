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



df = pd.read_csv("train.csv", index_col="RecipeId")
df.target = df.Target.astype('category')
df.head()









ITEMS = 15
cuisines=["","French","Italian","Indian","Chinese","Thai","Greek","Mexican"]
v = CountVectorizer(ngram_range=(1,3),max_features=ITEMS)
for i in range(1,8):
    df_x = v.fit_transform(df[df.Target == i].Ingredients.values.astype('U'))
    print("\nTop",ITEMS,"Ingredients for",cuisines[i],"Recipes")
    n = 1
    for ingr in sorted(v.vocabulary_.items(), key=operator.itemgetter(1)):
        print(n,ingr[0])
        n += 1







ITEMS = 50
v = TfidfVectorizer(sublinear_tf=True, ngram_range=(1,3),max_features=ITEMS)
df_x = v.fit_transform(df.Ingredients.values.astype('U'))
idf = v.idf_

topIngredients = pd.DataFrame({"Ingredient": v.get_feature_names(),"TfIdf":idf})
print("Top",ITEMS,"Ingredients")
topIngredients.sort_values(by="TfIdf",ascending=False)











nltk.download('punkt')

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = []
    for item in tokens:
        stems.append(PorterStemmer().stem(item))
    return stems

ITEMS = 50
v = TfidfVectorizer(sublinear_tf=True, tokenizer=tokenize, stop_words='english', ngram_range=(1,3),max_features=ITEMS)
df_x = v.fit_transform(df.Ingredients.values.astype('U'))
idf = v.idf_

topIngredients = pd.DataFrame({"Ingredient": v.get_feature_names(),"TfIdf":idf})
print("Top",ITEMS,"Ingredients")
topIngredients.sort_values(by="TfIdf",ascending=False)










 

df = pd.read_csv("train.csv", index_col="RecipeId")
df.target = df.Target.astype('category')













bestK = None
bestKMeanAcc = 0

v = CountVectorizer(max_features=100)
df_x = v.fit_transform(df.Ingredients.values.astype('U')).todense()

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
dfTrain = pd.read_csv("train.csv", index_col="RecipeId")
trainY = dfTrain.Target.astype('category')

dfTrain = dfTrain.drop(["Target"],axis=1)
df = pd.concat([dfTrain,pd.read_csv("test.csv", index_col="RecipeId")])

















v = CountVectorizer(max_features=100)
df_x = v.fit_transform(df.Ingredients.values.astype('U')).todense()

trainX = df_x[:len(dfTrain)]
testX = df_x[len(dfTrain):]










knn = KNeighborsClassifier(n_neighbors=7, weights='uniform', algorithm="auto")
knn.fit(trainX,trainY)

predictions = knn.predict(testX)










submissions = pd.read_csv("sampleSubmission.csv", index_col="RecipeId")
submissions.Target = predictions

submissions.to_csv("submission.csv")









# Load dataset
df = pd.read_csv("train.csv", index_col="RecipeId")

# Shuffle rows in dataset 
df = df.sample(frac=1)






v = CountVectorizer(max_features=100)
df_x = v.fit_transform(df.Ingredients.values.astype('U')).todense()






knn = KNeighborsClassifier(n_neighbors=7, weights='uniform', algorithm="auto")
predictions = cross_val_predict(knn, df_x, df.Target, cv=10)










pd.crosstab(predictions,df.Target,rownames=['Predictions'],colnames=['Actual Values'])





ITEMS = 15
cuisines=["","French","Italian","Indian","Chinese","Thai","Greek","Mexican"]

dfTest = df[int(len(df.index)*0.8):]

for prediction in range(1,8):
    for actual in range(1,8):
        v = CountVectorizer(max_features=ITEMS)
        if np.sum(np.logical_and(predictions==prediction,df.Target==actual)) > 0:
            df_cell = v.fit_transform(df[np.logical_and(predictions==prediction,df.Target==actual)].Ingredients.values.astype('U')).todense()
            print("\nTop",ITEMS,"Ingredients for",cuisines[actual],"classified as",cuisines[prediction])
            n = 1
            for ingr in sorted(v.vocabulary_.items(), key=operator.itemgetter(1)):
                print(n,ingr[0])
                n += 1

