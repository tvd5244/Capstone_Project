
# coding: utf-8

# In[81]:


import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier

from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier


import operator


import nltk
from nltk.stem.porter import PorterStemmer

from sklearn.model_selection import cross_val_predict

def tokenize(text):
    return text.split()


# In[141]:


df = pd.read_csv("train.csv", index_col="PersonID")


# In[88]:


class_names=np.array(["","Sports","Computer Nerds","Anime","Computer Science","Math","Theater","Sing and Dance","Music","Movies","Food"])
class_list = np.arange(len(class_names))


# In[71]:


count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(df.Interests)


# In[72]:


tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)


# In[73]:


clf = SGDClassifier().fit(X_train_tfidf, df.ClusterClassifier)


# In[74]:


#Prediction on training set
predicted = clf.predict(X_train_tfidf)
print("Accuracy on training set : {}".format(np.mean(predicted == df.ClusterClassifier)))


# In[82]:


#Reading the Test set
df_test = pd.read_csv("test.csv", index_col="PersonID")
new_df = df_test


# In[145]:


#Pipeline for the whole procedure. Using SGDClassifier for prediction.
text_clf_svm = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                    ('clf-svm', SGDClassifier())
                    ])


# In[146]:


#Training on train.csv
text_clf_svm = text_clf_svm.fit(df.Interests, df.ClusterClassifier)


# In[147]:


predictions = text_clf_svm.predict(df_test.Interests)
predictions


# In[148]:


#Grouping train.csv By Categories
group_by_type = df.groupby('ClusterClassifier')


# In[149]:


#Suggesting Friends by person ID to each of the person in test.csv

for row in df_test.iterrows():
    print("Person ID in test.csv : {} \n\t Predicted Class : {} \n\t Suggested Friends Person IDs : {}".format(row[0],class_names[predictions[row[0]-1]] ,list(group_by_type.get_group(row[0]).index)))


# In[150]:


new_df["Predicted_class"] = predictions
new_df["Similar_Friends"] = pd.Series([])


# In[151]:


list_friends = []
for i in range(len(new_df)):
    list_friends.append(list(group_by_type.get_group(new_df.iloc[i].iloc[1]).index))
new_df["Similar_Friends"] = list_friends
new_df["Predicted_class"] = class_names[predictions]

new_df.drop("Interests",axis = 1 ,inplace = True) #drops the interests column

# In[152]:


new_df.to_csv("final.csv")
