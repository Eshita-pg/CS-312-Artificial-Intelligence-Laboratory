#!/usr/bin/env python
# coding: utf-8

# In[20]:


import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score


# In[21]:


#read data
# data = pd.read_csv("spambase.csv")
url = "https://drive.google.com/file/d/1zhWZOSfIXSAbDIz-xI7o8HSOeV3dbpeJ/view?usp=drivesdk"
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]

data = pd.read_csv(path,header=None)


# In[22]:


data.info()


# In[23]:


data.isnull().sum()


# In[24]:


data.describe()


# In[25]:


#split test and train test
x = data.drop(data.columns[57], axis=1)
y = data.iloc[:,-1]

x_train, x_test, y_train ,y_test = train_test_split(x,y,test_size= 0.3)


# In[26]:


#define and train model
svclassifier = SVC(C= 0.01, kernel = 'linear')
svclassifier.fit(x_train, y_train)
#get prediction on test dataset
y_pred = svclassifier.predict(x_test)

print("FOR C= 0.01 AND KERNEL = 'LINEAR'")
print(classification_report(y_test,y_pred))


print("Accuracy Score: ")
print(accuracy_score(y_test, y_pred))


# In[27]:


svclassifier = SVC(C= 0.1, kernel = 'linear')
svclassifier.fit(x_train, y_train)
y_pred = svclassifier.predict(x_test)

print("FOR C= 0.1 AND KERNEL = 'LINEAR'")

print(classification_report(y_test,y_pred))
print("Accuracy Score: ")
print(accuracy_score(y_test, y_pred))


# In[ ]:


svclassifier = SVC(C= 0.5, kernel = 'linear')
svclassifier.fit(x_train, y_train)
y_pred = svclassifier.predict(x_test)
print("FOR C= 0.5 AND KERNEL = 'LINEAR'")

print(classification_report(y_test,y_pred))
print("Accuracy Score: ")
print(accuracy_score(y_test, y_pred))


# In[ ]:


svclassifier = SVC(C= 1, kernel = 'linear')
svclassifier.fit(x_train, y_train)
y_pred = svclassifier.predict(x_test)
print("FOR C= 1 AND KERNEL = 'LINEAR'")

print(classification_report(y_test,y_pred))
print("Accuracy Score: ")
print(accuracy_score(y_test, y_pred))


# In[ ]:


svclassifier = SVC(C= 0.5, kernel = 'poly', degree=2)
svclassifier.fit(x_train, y_train)
y_pred = svclassifier.predict(x_test)
print("FOR C= 0.5 AND KERNEL = 'POLY'")

print(classification_report(y_test,y_pred))
print("Accuracy Score: ")
print(accuracy_score(y_test, y_pred))


# In[ ]:


svclassifier = SVC(C= 50, kernel = 'poly', degree=2)
svclassifier.fit(x_train, y_train)
y_pred = svclassifier.predict(x_test)
print("FOR C= 50 AND KERNEL = 'POLY'")
print(classification_report(y_test,y_pred))
print("Accuracy Score: ")
print(accuracy_score(y_test, y_pred))


# In[ ]:


svclassifier = SVC(C= 5000, kernel = 'poly', degree=2)
svclassifier.fit(x_train, y_train)
y_pred = svclassifier.predict(x_test)
print("FOR C= 5000 AND KERNEL = 'POLY'")
print(classification_report(y_test,y_pred))
print("Accuracy Score: ")
print(accuracy_score(y_test, y_pred))


# In[ ]:


svclassifier = SVC(C= 50000, kernel = 'poly', degree=2)
svclassifier.fit(x_train, y_train)
y_pred = svclassifier.predict(x_test)
print("FOR C= 50000 AND KERNEL = 'POLY'")
print(classification_report(y_test,y_pred))
print("Accuracy Score: ")
print(accuracy_score(y_test, y_pred))


# In[ ]:


svclassifier = SVC(C= 0.5, kernel = 'rbf')
svclassifier.fit(x_train, y_train)
y_pred = svclassifier.predict(x_test)
print("FOR C= 0.5 AND KERNEL = 'RBF'")
print(classification_report(y_test,y_pred))
print("Accuracy Score: ")
print(accuracy_score(y_test, y_pred))


# In[ ]:


svclassifier = SVC(C= 50, kernel = 'rbf')
svclassifier.fit(x_train, y_train)
y_pred = svclassifier.predict(x_test)
print("FOR C= 50 AND KERNEL = 'RBF'")
print(classification_report(y_test,y_pred))
print("Accuracy Score: ")
print(accuracy_score(y_test, y_pred))


# In[ ]:


svclassifier = SVC(C= 5000, kernel = 'rbf')
svclassifier.fit(x_train, y_train)
y_pred = svclassifier.predict(x_test)
print("FOR C= 5000 AND KERNEL = 'RBF'")
print(classification_report(y_test,y_pred))
print("Accuracy Score: ")
print(accuracy_score(y_test, y_pred))


# In[ ]:


svclassifier = SVC(C= 50000, kernel = 'rbf')
svclassifier.fit(x_train, y_train)
y_pred = svclassifier.predict(x_test)
print("FOR C= 50000 AND KERNEL = 'RBF'")
print(classification_report(y_test,y_pred))
print("Accuracy Score: ")
print(accuracy_score(y_test, y_pred))


# In[ ]:


# checking accuracies for all kernels and C values in single function
# c_value = [0.01, 0.1, 0.5, 1, 50, 5000, 50000]
# kernals = ['linear', 'poly', 'rbf']
# svclassifier = SVC(C= a , kernel = 'linear')
# svclassifier.fit(x_train, y_train)
# prediction = []
# def svc(C_val,Kernel):
#     for k in Kernel:
#         for c in C_val:
#             if k == "poly":
#                 svclassifier = SVC(C = c , kernel=k , degree=2)
#             else:    
#                 svclassifier = SVC(C = c , kernel=k)
                
#             svclassifier.fit(x_train, y_train)
#             y_pred = svclassifier.predict(x_test)
#             print(classification_report(y_test,y_pred))
#             prediction.append(svclassifier.predict(x_test))
#             print(prediction)
            
# svc(c_value , kernals)

