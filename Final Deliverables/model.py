import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
data=pd.read_csv('C:/Users/Lenovo/OneDrive/Documents/Nalaiya Thiran/University
Admit Eligibility Predictor/dataset/Admission_predict.csv')
data.drop(["Serial No."],axis=1,inplace=True)
df = pd.DataFrame(data)
df.columns = df.columns.str.replace(' ', '_')
df['result']=pd.cut(df.Chance_of_Admit_,bins=[0,0.80,1],labels=['No','Yes'])
independent = data.iloc[:,0:7].values
dependent = data.iloc[:,8:].values
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(independent, dependent,
random_state=0, train_size = .2)
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
trained_model = rf.fit(X_train, y_train)
pickle.dump(rf, open('university.pkl','wb'))