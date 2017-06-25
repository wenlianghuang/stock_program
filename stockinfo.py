from urllib.request import urlopen
from bs4 import BeautifulSoup 
import requests 
import matplotlib.pyplot as plt 
import numpy as np
from stock_plot import Plot 
import math 
import csv 
import datetime
class Stockinfo:
  def __init__(self,filename,protype):
    self.protype = protype
    self.filename = filename
  def readfile(self):
    opfile = open(self.filename,'r')
    content = opfile.readlines()
    
    #stocks = [x.strip() for x in content] 
    for i in range(len(content)):
      #get rid of "\n"
      content[i] = content[i].rstrip()
      content[i] = content[i].split(',')
      #Make a list with default len(content) number of element and store stock number 
      stocks = [content[i][0] for i in range(len(content))]
      #Make a list with default len(content) number of element and store shares number 
      shares = [content[i][1] for i in range(len(content))]
    self.stocks = stocks
    self.shares = shares 

  def getweburl(self):
    web_url = []
    for i in range(len(self.stocks)):
      web_url.append('http://cnyes.com/twstock/'+self.stocks[i]+".htm")
    self.web_url = web_url
  def date_info(self):
    fmt = '%Y-%m-%d' #datetime for we want to transform to.
    today = datetime.date.today()
    dayorg = datetime.datetime.strptime('1970-1-1',fmt)#This is for the javascript first day.
    daystart = datetime.datetime.strptime(str(today.year)+'-'+str(today.month-4)+'-'+str(today.day),fmt)#To fit the form for strptime
    dayend = datetime.datetime.strptime(str(today),fmt)
    period1 = (daystart-dayorg).days*86400
    period2 = (dayend-dayorg).days*86400
    self.period1 = period1
    self.period2 = period2
    todayy = str(today.year)
    todaym = str(today.month)
    todayd = str(today.day)
    today = str(today)
    self.today = today
    self.todayy = todayy
    self.todaym = todaym
    self.todayd = todayd
    
    #Reference: https://docs.python.org/2/library/datetime.html

  def daily_price(self):
    table_con = [0 for x in range(len(self.web_url))]
    table_detail = [0 for x in range(len(self.web_url))]
    table_tr = [0 for x in range(len(self.web_url))]
    hist_price = [ [] for x in range(len(self.web_url))]
    date = [ [] for x in range(len(self.web_url))]
    stock_name = [0 for x in range(len(self.web_url))]
    web_url = [' ' for x in range(len(self.web_url))]
    amplitude = [ [] for x in range(len(self.web_url))]
    todayprice = [0 for x in range(len(self.web_url))]
    yesprice = [0 for x in range(len(self.web_url))]
    weekprice = [0 for x in range(len(self.web_url))]
    monthprice = [0  for x in range(len(self.web_url))]
    for i in range (len(self.web_url)):
      web_url[i] = self.web_url[i][:25]+"ps_historyprice/"+self.web_url[i][25:]
    for i in range(len(self.web_url)):
      html = urlopen(web_url[i])
      bsObj = BeautifulSoup(html,"html.parser")
      table_con[i] = bsObj.find("table",{"enableviewstate":"false"})
      table_detail[i] = table_con[i].findAll("td")
      table_tr[i] = table_con[i].findAll("tr")
      stock_name[i] = bsObj.find("div",{"class","strName"}).findAll("a",href="/twstock/profile/"+self.stocks[i]+".htm")
      stock_name[i] = stock_name[i][0].get_text()
      for j in range(0,len(table_detail[i]),10):
        date[i].append(table_detail[i][j].get_text())
        hist_price[i].append(float(table_detail[i][j+4].get_text()))
        amplitude[i].append(table_detail[i][j+6].get_text())
        date[i][int(j/10)] = date[i][int(j/10)].split('/')
        date[i][int(j/10)] = date[i][int(j/10)][1]+date[i][int(j/10)][2]
        amplitude[i][math.floor((j+6)/10)] = amplitude[i][math.floor((j+6)/10)].split("%")
        amplitude[i][math.floor((j+6)/10)] = float(amplitude[i][math.floor((j+6)/10)][0])
      todayprice[i] = hist_price[i][0]
      yesprice[i]  = hist_price[i][1]
      weekprice[i] = hist_price[i][5]
      hispri_plot = Plot(date[0],self.stocks[i],"history_price",stock_name[i])
      hispri_plot.histprice_plot(hist_price[i],amplitude[i])
    stock_name.insert(0,' ')
    self.shares.insert(0,"Shares")
    todayprice.insert(0,"Toady price")
    yesprice.insert(0,"Yesterday price")
    weekprice.insert(0,"Weekbef price")

    csvfile1 = open("account.csv","w")
    csvCursor = csv.writer(csvfile1)
    csvCursor.writerow(stock_name)
    csvCursor.writerow(self.shares)
    csvCursor.writerow(todayprice)
    csvCursor.writerow(yesprice)
    csvCursor.writerow(weekprice)
    csvfile1.close()
  
  
  #ttday:totay day I want to choose for calculating EMA
  #daybefore: How many days I want for ema(12/26/9)
  #flagday: Just a day counter
  def EMA(self,price_list,ttday,daybefore,flagday,EMAlist):
    multiplier = 2/(daybefore+1)
    EMAvalue = 0
    if((ttday-flagday) == daybefore):
      for i in range(daybefore):
        if(daybefore == 9):#This is for DEM because it start day is not 9 but 26
          EMAvalue +=price_list[ttday-i-26] #26 is for the first 26 day
        else:
          EMAvalue += price_list[ttday-i-1]
      EMAvalue = (EMAvalue/daybefore)
      EMAlist.append(EMAvalue)
      return EMAvalue
    else:
      flagday  +=1
      EMAtruevalue = self.EMA(price_list,ttday,daybefore,flagday,EMAlist)
      flagday -=1 #To fit the close price of current day after the EMA 
      EMAlist.append((price_list[ttday-flagday-1]-EMAtruevalue)*multiplier+EMAtruevalue)

      return (price_list[ttday-flagday-1]-EMAtruevalue)*multiplier+EMAtruevalue
  def MACDline(self,jun3p):
    hist_price = []
    html = urlopen('https://finance.yahoo.com/quote/2104.TW/history?period1='+str(self.period1)+'&period2='+str(self.period2)) #This program I choose Yahoo finance for data source 
    bsObj = BeautifulSoup(html,"html.parser")
    table_detail = bsObj.find("table",{"W(100%) M(0) BdB Bdc($lightGray)"}).findAll("span")
    for i in range(7,len(table_detail),7):
      if(float(table_detail[i+4].get_text()) == 0):
        hist_price.append(jun3p)
        continue
      hist_price.append(float(table_detail[i+4].get_text()))
    #print(hist_price)
    flagtoday = 0
    print(len(hist_price))
    EMAlist = []
    EMAlist2 = []
    DIFlist = []
    DEMlist = []
    self.EMA(hist_price,len(hist_price),12,flagtoday,EMAlist)
    flagtoday = 0
    self.EMA(hist_price,len(hist_price),26,flagtoday,EMAlist2)
    for i in range(len(hist_price)-len(EMAlist)):
      EMAlist.append(0)
    EMAlist.reverse()
    for i in range(len(hist_price)-len(EMAlist2)):
      EMAlist[i] = 0
      EMAlist2.append(0)
    EMAlist2.reverse() #Reverse first and combine with EMAlist for DIFlist 
    for i in range(len(hist_price)):
      DIFlist.append(EMAlist[i]-EMAlist2[i])
    DIFlist.reverse() #Reverse for calculating DEM(EMA(DIF,9))
    flagtoday = 26
    self.EMA(DIFlist,len(hist_price),9,flagtoday,DEMlist)
    DIFlist.reverse()
    for i in range(len(hist_price)-len(DEMlist)):
      DEMlist.append(0)
    DEMlist.reverse()
    #print(DIFlist)
    #print(DEMlist)
    macd = Plot(5,10,15,20)#The detail put in plot need to be adjust latter
    macd.MACDPlot(DIFlist,DEMlist)
