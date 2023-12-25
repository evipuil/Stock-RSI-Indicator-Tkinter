#Resources Used
#https://algotrading101.com/learn/yahoo-finance-api-guide/ - Yahoo Finance API Usage
#https://matplotlib.org/stable/tutorials/introductory/pyplot.html - Matplotlib Documentation
#https://www.geeksforgeeks.org/introduction-to-pandas-in-python/ - Pandas and Numpy Documentation

#Importing the necessary libraries
from tkinter import * #Graphics Library
import yfinance as yf #Stock Price Library
import pandas as pd #Accessing Stock Price
import numpy as np #Converting list to array
import matplotlib.pyplot as plt #Graphing the prices from the array
from datetime import datetime #Accessing data from specific dates
from ta.momentum import RSIIndicator #Finding RSI

#Graphics Formatting
window=Tk()
window.geometry("600x600")

title=Label(window, text="Stock Lookup", font="Times 30")
title.grid(row=0, column=0)

inputLabel=Label(window, text="Enter the Stock Symbol", font="Times 20")
inputLabel.grid(row=1, column=0)

input=Entry(window, width=40)
input.grid(row=2, column=0)

lbl1=Label(window, text="*** Stock Indicators ***", font="Times 20")
lbl1.grid(row=4, column=0)

RSILabel=Label(window, text="RSI: ", font="Times 18")
RSILabel.grid(row=5, column=0)

MA20=Label(window, text="20-day Moving Average: ", font="Times 18")
MA20.grid(row=6, column=0)

MA50=Label(window, text="50-day Moving Average: ", font="Times 18")
MA50.grid(row=7, column=0)

MA200=Label(window, text="200-day Moving Average: ", font="Times 18")
MA200.grid(row=8, column=0)

CP=Label(window, text="Current Price: ", font="Times 18")
CP.grid(row=9, column=0)

#Procedure that remove empty values from a list
def cleanup(list):
  newList=[]
  for i in range(0, len(list)-1):
    if list[i]!=None:
      newList.append(list[i])
  return newList  

#Finds the RSI
def check_rsi(ticker):
    data = yf.download(ticker, period='1d', interval='1m')
    rsi = RSIIndicator(data['Close']).rsi()
    return (rsi.iloc[-1])

#Finds the Moving Average using a list of prices and a specific period of days
def movingAverage(list, period):
  list=list[-period:]
  total=0
  for i in range(len(list)):
    total+=list[i]
  return(total/period)

#Looks up the stock prices, creates a graph, and uses the prices to display the indicators
def lookup():
  stock=input.get()
  symbol=yf.Ticker(stock)
  history=symbol.history(period="max", interval="1d") #Finds the stock prices in a pandas dataframe
  history=pd.DataFrame(history)
  prices=history.Open #Removes unnecessary data
  x=[]
  y=[]
  date=datetime.today().strftime('%Y-%m-%d') #Today's date
  currentprice=prices.get(date)
  if type(currentprice) is int:
      currentprice=round(currentprice, 1)
  for i in range(10000):
    y.append(prices.get(date)) #Adds Stock Prices
    x.append(date) #Adds Dates
    #Changes the Date
    monthday=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    year=int(date[0:4])
    month=int(date[5:7])
    day=date[8:]
    day=int(date[8:])
    if day%4==0:
      monthday[2]=29 #Leap Year
    if day==1:
      if month==1:
        month==12
        day=monthday[month-1]
        year-=1
      else:
        day=monthday[month-2]
        month-=1
    else:
      day-=1
    if len(str(month))==1:
      month="0"+str(month)
    if len(str(day))==1:
      day="0"+str(day)
    date=str(year)+"-"+str(month)+"-"+str(day)
  y=cleanup(y)
  if len(y)!=0: #Checks if stock is valid
    RSILabel.configure(text="RSI: ")
    y.reverse()
    ma20=round(movingAverage(y, 20), 1)
    ma50=round(movingAverage(y, 50), 1)
    ma200=round(movingAverage(y, 200), 1)
    MA20.configure(text="20-day Moving Average: "+str(ma20)) #Displays 20-day Moving Average
    MA50.configure(text="50-day Moving Average: "+str(ma50)) #Displays 50-day Moving Average
    MA200.configure(text="200-day Moving Average: "+str(ma200)) #Displays 200-day Moving Average
    actualrsi=round(check_rsi(stock), 1) #Finds and rounds the RSI
    rsi="RSI: "+str(actualrsi)
    RSILabel.configure(text=rsi) #Displays the RSI
    CP.configure(text="Current Price: "+str(currentprice))
    newx=[]
    for k in range(len(y)):
      newx.append(x[k])
    newx.reverse()
    newx=newx[len(newx)-len(y):]
    y=np.array(y) #Creates numpy array
    x=np.array(newx) #Creates numpy array
    plt.plot(x, y) #Creates a graph
    plt.show() #Displays the in a new Tkinter window
  else: #If there is an invalid stock symbol
    RSILabel.configure(text="Invalid Stock")
    MA20.configure(text="20-day Moving Average: N/A")
    MA50.configure(text="50-day Moving Average: N/A")
    MA200.configure(text="200-day Moving Average: N/A")
    CP.configure(text="Current Price: N/A")
  

button=Button(text="Find", command=lookup, font="Times 18") #Tkinter Button to Lookup Stock
button.grid(row=3, column=0)
