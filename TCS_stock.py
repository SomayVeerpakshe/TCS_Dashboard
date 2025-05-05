# Importing Yfinance library - to get stock data
import yfinance as yf
# Importing Pandas - to store data and clean data
import pandas as pd
#Importing Matplotlib for data visualization
import matplotlib.pyplot as plt 
# Importing date from datetime library
from datetime import date
# Importing stock symbol's file for NIFTY 50
#from Getting_stock_symbol import symbols

sy = "TCS.NS"
stock_financials = yf.Ticker(sy)
balance_sheet = stock_financials.balance_sheet
#tcs.to_csv(r"C:\Users\somay\Desktop\Data Science\Personal_Data_Projects\Project - Stock Market Pattern Predictor\TCS\TCS_balance_sheet.csv")

# Getting Stock info
indicators_list = ["longName","industry","sector","trailingPE","forwardPE","marketCap","profitMargins","trailingEps","totalDebt","quickRatio","currentRatio","totalRevenue","marketCap"]
required_indicators = {}

indicators = stock_financials.info
for i in indicators_list:
    required_indicators[f"{i}"] = indicators[i]
    #print(f"{i} : ", indicators[i])

tcs_df = pd.Series(required_indicators)
#print(tcs_df)

#Creating function to get the Stock Info like Name, Industry, Sector, PE ratio, Market Cap, Profit Margin

def indicators(data):
    if isinstance(required_indicators[data],float):
        return round(required_indicators[data],2)
    else:
        return required_indicators[data]
print(indicators("trailingPE"))

def valuation():
    valuation = stock_financials.financials.drop(columns=["2021-03-31"])
    required_fundamentals = valuation.loc[["Net Income","Total Revenue","Gross Profit"]]
    return required_fundamentals
#print(required_fundamentals)
print(valuation())
print(valuation().loc["Net Income"])
#Calculating CAGR for NetProfit and revenue
# 1. Netprofit
starting_net_profit = valuation().iloc[0,3]
ending_net_profit = valuation().iloc[0,0]


# 2. Revenue
starting_revenue = valuation().iloc[1,3]    
ending_revenue = valuation().iloc[1,0]

# CAgr formula
def cagr(x,y,n):
    growth = (((y/x)** (1/n)) - 1)*100
    return growth

cagr_profit = cagr(starting_net_profit,ending_net_profit,4)
cagr_revenue = cagr(starting_revenue,ending_revenue,4)
print(cagr_profit)
#print(cagr_revenue)

#Creating a Function to Fetch stock data of TCS from 2025 April 20 to 2021 April 20

def stock_data(i):
    stock_data = yf.download(i,start=date(2021,4,20), end = date(2025,4,20))
    stock_data.reset_index(inplace=True)
    stock_df = stock_data.xs(f"{i}",axis=1, level='Ticker').copy()
    stock_df["Symbol"] = i
    stock_df["Date"] = stock_data["Date"]
    stock_df = stock_df[["Date","Symbol","Open","High","Close","Volume"]]
    return stock_df
    
i = "TCS.NS"
TCS_OHLC_data = stock_data(i)
        