from urllib.request import urlopen
from bs4 import BeautifulSoup 
import requests 
import matplotlib.pyplot as plt 
import numpy as np
from stock_plot import Plot 
import math 
import csv 
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
    for i in range (len(self.web_url)):
      web_url[i] = self.web_url[i][:25]+"ps_historyprice/"+self.web_url[i][25:]
      #print(web_url[i])
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
      #print(hist_price[i][0])
      todayprice[i] = hist_price[i][0]
      yesprice[i]  = hist_price[i][1]
      hispri_plot = Plot(date[0],self.stocks[i],"history_price",stock_name[i])
      hispri_plot.histprice_plot(hist_price[i],amplitude[i])
    #Insert element at the first place("0")
    #print(todayprice)
    self.shares.insert(0,"Shares")
    stock_name.insert(0,' ')
    todayprice.insert(0,"Toady price")
    yesprice.insert(0,"Yesterday price")
    csvfile1 = open("account.csv","w")
    csvCursor = csv.writer(csvfile1)
    csvCursor.writerow(stock_name)
    csvCursor.writerow(self.shares)
    csvCursor.writerow(todayprice)
    csvCursor.writerow(yesprice)
    csvfile1.close()
