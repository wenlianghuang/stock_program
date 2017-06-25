import csv
import math
from datetime import datetime,date 
class Myaccount:

  def __init__(self,filename):
    self.filename = filename 
  def somevalue(self):
    csvfilerea = open(self.filename,'r')
    #csvreader = csv.reader(csvfile,delimiter=',')
  
    
    csvreader = csv.reader(csvfilerea)
    #csv.reader it is an iterator over the row, we have to convert it to list 
    data_list = list(csvreader)
    for i in range(len(data_list[0])-1):
    #tdvalue = share * today_price*1000
      tdvalue = [math.floor((float(data_list[1][i+1])*float(data_list[2][i+1])*1000)) for i in range(len(data_list[0])-1)]
    #ydvalue = share * yesterday_price*1000
      ydvalue = [math.floor((float(data_list[1][i+1])*float(data_list[3][i+1])*1000)) for i in range(len(data_list[0])-1)]
      weekvalue = [math.floor((float(data_list[1][i+1])*float(data_list[4][i+1])*1000)) for i in range(len(data_list[0])-1)]
      #monthvalue = [math.floor((float(data_list[1][i+1])*float(data_list[5][i+1])*1000)) for i in range(len(data_list[0])-1)]
      pro_los = [(tdvalue[i]-ydvalue[i]) for i in range(len(data_list[0])-1)]
      pro_losw = [(tdvalue[i]-weekvalue[i]) for i in range(len(data_list[0])-1)]
      #pro_losm = [(tdvalue[i]-monthvalue[i]) for i in range(len(data_list[0])-1)]
    self.tdvalue = tdvalue
    self.ydvalue = ydvalue
    self.pro_los = pro_los
    self.pro_losw = pro_losw
    #self.pro_losm = pro_losm
    csvfilerea.close()
  def daily_pro_loss(self):
    self.tdvalue.insert(0,'Today Stock Value')
    self.pro_los.insert(0,'Profits or Losses(D)')
    self.pro_losw.insert(0,'Profits or Losses(W)')
    #self.pro_losm.insert(0,'Profits or Losses(M)')
    with open(self.filename,'a') as csvfilewri:
      csvwriter = csv.writer(csvfilewri)
      csvwriter.writerow(self.tdvalue)
      csvwriter.writerow(self.pro_los)
      csvwriter.writerow(self.pro_losw)
      #csvwriter.writerow(self.pro_losm)
    csvfilewri.close() 
def main():
  aa = Myaccount("account.csv")
  aa.somevalue()
  aa.daily_pro_loss()
if __name__ == '__main__':
  main()



