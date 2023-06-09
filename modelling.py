# -*- coding: utf-8 -*-
"""Modelling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HxAsUKmya8X8cUG1bMRJR7j4BH1q8qxX
"""

# importing the dependencies
import math
import xgboost as xgb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

#load libraries
import numpy as np 
import pandas as pd

from scipy import stats
from scipy.stats import norm

from google.colab import drive
drive.mount('/content/drive')

# loading preprocessed train data
df = pd.read_csv('/content/drive/MyDrive/preprocessed_data.csv')

df['data'] = df['data'].fillna('')

df.head()

# vectorization - converting textual data into vectors

cv = CountVectorizer(max_features=500000)

X_train_vec = cv.fit_transform(df['data'])

# using xbBoost regression algorithm for prediction

xgbr = xgb.XGBRegressor(objective='reg:squarederror', colsample_bytree=0.8,
                        learning_rate=0.1,
                        max_depth=35, alpha=1, n_estimators=100)

# Training the model
xgbr.fit(X_train_vec, df['PRODUCT_LENGTH'])

# Loading the Preprocessed testing data
test_df = pd.read_csv('/content/drive/MyDrive/preprocessed_test_data.csv')

test_df = test_df.fillna('')

# Vectorizing textual data present in testing data

x_test = cv.transform(test_df['CONTENT'])
x_test.shape

# Predicting Product length -> Target variable

product_length = xgbr.predict(x_test)
product_length

# Converting product length to actual format
product_length = pow(math.exp(1), product_length)
product_length

# Converting to dataframe of specified format

data_frame = pd.DataFrame(product_length, columns=['PRODUCT_LENGTH'])
data_frame['PRODUCT_ID'] = test_df["PRODUCT_ID"]
data_frame = data_frame.loc[:,['PRODUCT_ID', 'PRODUCT_LENGTH']]
data_frame

# Saving the final result
data_frame.to_csv('final_result.csv', index=False)