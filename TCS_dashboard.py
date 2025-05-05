import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import streamlit as st
# Gathering data from TCS
import TCS_stock as tcs

# Set the page config
st.set_page_config(page_title="TCS Dashboard", layout="wide")

# Getting Close prices data of TCS, Moving Average of 200 days & 50 days 
i = "TCS.NS"
# --------------------Caching the data------------------

# Creating a Caching function to get the stock data
# This will help to load the data faster and avoid reloading it every time
@st.cache_data

def get_stock_data(i):
    TCS_OHLC_data = tcs.stock_data(i)
    TCS_OHLC_data["50_MA"] = TCS_OHLC_data["Close"].rolling(window=50).mean()
    TCS_OHLC_data["200_MA"] = TCS_OHLC_data["Close"].rolling(window=200).mean()
    return TCS_OHLC_data

@st.cache_data

def get_indicators(indicator):
    f = tcs.indicators(indicator)
    return f

@st.cache_data
def get_fundamentals():
    return tcs.valuation()

#-------------------Fetching the data-------------------

# Getting OHLC and Moving Average data of TCS
TCS_OHLC_data = get_stock_data(i)

# Getting the stock indicators like PE ratio, Market Cap, Profit Margin, Industry PE ratio
pe_ratio = get_indicators("trailingPE")
industry_pe = 29.6
name = get_indicators("longName")
industry = get_indicators("industry")
sector = get_indicators("sector")
market_cap = get_indicators("marketCap")   
profit_margin = get_indicators("profitMargins")

#Fundamentals of TCS last 4 year data from 31 March 2021 to 31 March 2025
tcs_fundamentals = get_fundamentals()
years = [2025,2024,2023,2022]
net_profit_4years = tcs_fundamentals.loc["Net Income"]
revenue_4years = tcs_fundamentals.loc["Total Revenue"]
# Making Bargraph of Net Profit and Revenue
fig, ax = plt.subplots(figsize=(10,5))
x = np.arange(len(years))
width = 0.4
ax.bar(x-width/2 ,net_profit_4years,width,label = "Net Profit",color = "mediumseagreen")
ax.bar(x+width/2,revenue_4years,width,label = "Revenue",color = "aquamarine")
ax.set_xlabel("Years")
ax.set_ylabel("Net Profit vs Revenue 4 years")
ax.set_xticks(x,years)

# CAGR for NetProfit and revenue
# 1. Netprofit
starting_net_profit = tcs_fundamentals.iloc[0,3]
ending_net_profit = tcs_fundamentals.iloc[0,0]
net_profit = ending_net_profit
# 2. Revenue
starting_revenue = tcs_fundamentals.iloc[1,3]    
ending_revenue = tcs_fundamentals.iloc[1,0] 
revenue = ending_revenue

# CAgr formula
def cagr(x,y,n):
    growth = (((y/x)** (1/n)) - 1)*100
    return growth
#CAGR for NetProfit and Revenue
cagr_profit = cagr(starting_net_profit,ending_net_profit,4)
cagr_revenue = cagr(starting_revenue,ending_revenue,4)


# Building the Streamlit Dashboard
# -------------- Streamlit App ----------------



# Set the title and header
st.title("TCS Dashboard stock data from 2021 to 2025")
# Set the Name of Dashboard, Industry, Sector
st.write("Name: ", name)
st.write("Industry: ", industry)
st.write("Sector: ", sector)   

# Setting the layout of the dashboard, creating 3 columns
col1, col2, col3 = st.columns([2,2,1])

# Adding the TCS stock data to the first column OHLC data with moving average
with col1:
    st.subheader("TCS Stock Data")
    #st.line_chart(TCS_OHLC_data["Close"])
    st.subheader("TCS Moving Average")
    st.line_chart(TCS_OHLC_data[["Close","50_MA","200_MA"]])
    st.caption("TCS Stock Data from 2021 to 2025")
#st.dataframe(stock_data)
#st.subheader("TCS Financial Indicators")
#st.write("TCS Financial Indicators")    

# Adding The TCS Fundamentals to the second column like Net Profit, Revenue over years
with col2:
    st.subheader("TCS Fundamentals")    
    st.pyplot(fig,bbox_inches='tight')
    st.caption("Net Profit and Revenue over 4 years")
    

with col3:
    st.subheader("TCS Financial Indicators")
    st.write("PE Ratio: ", pe_ratio)
    st.write("Industry PE Ratio: ", industry_pe)
    st.write("Market Cap: ", market_cap)
    st.write("Profit Margin: ", profit_margin)
    st.write("CAGR for Net Profit: ", round(cagr_profit,2),"%")
    st.write("CAGR for Revenue: ", round(cagr_revenue,2),"%")
    st.write("Net Profit for this year: ", net_profit)
    st.write("Revenue for this year: ", revenue)    


