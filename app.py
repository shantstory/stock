import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
from keras.models import load_model
import streamlit as st

import yfinance as yf
yf.pdr_override()
start = '2010-01-01'
end = '2019-12-31'

st.title('stock Trend Prediction')
user_input=st.text_input('Enter stock Ticker','APPL')
df = pdr.get_data_yahoo(user_input, start="2010-01-01", end="2019-12-31")
st.subheader('Date from 2010 - 2019')
st.write(df.describe())

st.subheader ('Closing Price vs Time Chart ma100')
ma100=df.Close.rolling(100).mean()
fig=plt.figure(figsize=(12,6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)

st.subheader ('Closing Price vs Time Chart ma200')
ma100=df.Close.rolling(100).mean()
ma200=df.Close.rolling(200).mean()
fig=plt.figure(figsize=(12,6))
plt.plot(ma100 , 'r')
plt.plot(ma200, 'g' )
plt.plot(df.Close , 'b')
st.pyplot(fig)

data_training=pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing=pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler(feature_range=(0,1))
data_training_array=scaler.fit_transform(data_training)



model= load_model('keras_model.h5')
past_100_days=data_training.tail(100)
final_df=past_100_days.append(data_testing , ignore_index=True)
input_data=scaler.fit_transform(final_df)
x_test=[]
y_test=[]
for i in range(100,input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i,0])
x_test,y_test=np.array(x_test),np.array(y_test)
#making prediction
y_predicted=model.predict(x_test)
scaler=scaler.scale_
scale_factor=1/scaler[0]
y_predicted=y_predicted*scale_factor
y_test=y_test*scale_factor

st.subheader('Prediction vs Original')
fig2=plt.figure(figsize=(12,6))
plt.plot(y_test,'b',label="Original Price")
plt.plot(y_predicted,'r',label="Predicted Price")
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)


    
    

    

 


