#!/usr/bin/env python
# coding: utf-8

# In[78]:


# This Program predicts stock prices in the NSE by using Machine learning models
# Installing dependencies
import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split


# In[92]:


# Get the stock data
meta = yf.Ticker("META")
# Take a look at the data
df = meta.history(period="max")
print(df.head())


# In[80]:


# Get the Close Price
df = df[['Close']]
#Check new data
print(df.head())


# In[81]:


# A variable for predicting 'n' days out into the future
forecast_out = 30
# Create another column (the target or dependent variable) shifted 'n' units up
df['Prediction'] = df[['Close']].shift(-forecast_out)
#print the new data set
print(df.tail())


# In[82]:


### Create the Independent data set (X) ####
#### Convert the data frame into a numpy array
X = np.array(df.drop(columns=['Prediction']))
# Remove the last 'n' rows
X = X[:-forecast_out]
print(X)


# In[83]:


# Create the Dependent data set (y) ####
# Convert the data frame to a numpy array (All the values including the NaN's
y = np.array(df['Prediction'])
# Get all of the y values except the last 'n' rows
y = y[:-forecast_out]
print(y)


# In[84]:


# Split the data into 80% Traininga nd 20% Testing
x_train, x_test, y_train, y_test = train_test_split(X,y,test_size=0.2)


# In[85]:


# Create and traine the Support Vector Machine (Regressor)
svr_rbf = SVR(kernel='rbf',C=1e3,gamma=0.1)
svr_rbf.fit(x_train,y_train)


# In[86]:


#Testing Model: Score Returns the coefficient of the determination R^2 of the prediction
# The best possible score is 1.0
svm_confidence = svr_rbf.score(x_test,y_test)
print("svm_confidence: ",svm_confidence)


# In[87]:


# Create and train the Linear regression model
lr = LinearRegression()
# Train the model
lr.fit(x_train,y_train)


# In[88]:


#Testing Model: Score Returns the coefficient of the determination R^2 of the prediction
# The best possible score is 1.0
lr_confidence = lr.score(x_test,y_test)
print("lr_confidence: ",lr_confidence)


# In[89]:


# Set x_forecast equal to the last 30 rows of the original data set from the Close column
x_forecast = np.array(df.drop(columns=['Prediction'])[-forecast_out:])
print(x_forecast)


# In[90]:


# Print the linear predictions model for the next 'n' days
lr_prediction = lr.predict(x_forecast)
print(lr_prediction)


# In[91]:


# Print the support vector regressor  model for the next 'n' days
svm_prediction = svr_rbf.predict(x_forecast)
print(svm_prediction)


# In[93]:


#### Create App.py
import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Stock Price Predictor", layout="wide")

st.title("📈 Stock Price Prediction using Machine Learning")

# ---------------- UI INPUTS ----------------
ticker = st.text_input("Enter Stock Ticker", value="META")
forecast_out = st.slider("Forecast Days", 7, 90, 30)

model_type = st.selectbox(
    "Choose Model",
    ["Linear Regression", "Support Vector Regression (RBF)"]
)

run = st.button("Run Prediction")

# ---------------- MAIN LOGIC ----------------
if run:
    with st.spinner("Downloading data & training model..."):
        stock = yf.Ticker(ticker)
        df = stock.history(period="max")

        if df.empty:
            st.error("No data found for this ticker.")
            st.stop()

        df = df[['Close']]
        df['Prediction'] = df[['Close']].shift(-forecast_out)

        X = np.array(df.drop(columns=['Prediction']))
        X = X[:-forecast_out]
        y = np.array(df['Prediction'])[:-forecast_out]

        x_train, x_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        if model_type == "Linear Regression":
            model = LinearRegression()
        else:
            model = SVR(kernel='rbf', C=1e3, gamma=0.1)

        model.fit(x_train, y_train)
        confidence = model.score(x_test, y_test)

        x_forecast = np.array(df.drop(columns=['Prediction'])[-forecast_out:])
        prediction = model.predict(x_forecast)

    # ---------------- OUTPUT ----------------
    st.success("Prediction complete ✅")

    col1, col2 = st.columns(2)
    col1.metric("Model", model_type)
    col2.metric("R² Score", f"{confidence:.3f}")

    forecast_df = pd.DataFrame({
        "Day": range(1, forecast_out + 1),
        "Predicted Close": prediction
    })

    st.subheader("📊 Forecast Data")
    st.dataframe(forecast_df)

    # ---------------- CHART ----------------
    import pandas as pd
import matplotlib.pyplot as plt

# Last known date in the dataset
last_date = df.index[-1]

# Infer frequency (falls back to business days if None)
freq = pd.infer_freq(df.index)
if freq is None:
    freq = "B"

# Create future dates matching forecast length
import pandas as pd

# Number of forecast points (safe)
n_forecast = len(lr_prediction)

last_date = df.index[-1]

freq = pd.infer_freq(df.index)
if freq is None:
    freq = "B"

future_dates = pd.date_range(
    start=last_date,
    periods=n_forecast + 1,
    freq=freq
)[1:]

forecast_df = pd.DataFrame(
    lr_prediction.reshape(-1),
    index=future_dates,
    columns=["Predicted Close"]
)

# Build forecast DataFrame with proper datetime index
forecast_df = pd.DataFrame(
    lr_prediction, 
    index=future_dates, 
    columns=["Predicted Close"]
)

# ---------------- Plot ----------------
fig, ax = plt.subplots(figsize=(12, 5))

df["Close"].tail(200).plot(ax=ax, label="Historical Close")
forecast_df["Predicted Close"].plot(ax=ax, label="Forecast", color="red")

ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.legend()

st.pyplot(fig)


# In[ ]:




