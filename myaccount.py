import csv
import math
class Myaccount:

  def __init__(self,filename):
    self.filename = filename 
  def somevalue(self):
    csvfile = open(self.filename,'r')
    #csvreader = csv.reader(csvfile,delimiter=',')
  
    
    csvreader = csv.reader(csvfile)
    #csv.reader it is an iterator over the row, we have to convert it to list 
    data_list = list(csvreader)
    for i in range(len(data_list[0])-1):
    #tdvalue = share * today_price*1000
      tdvalue = [(float(data_list[1][i+1])*float(data_list[2][i+1])*1000) for i in range(len(data_list[0])-1)]
    #ydvalue = share * yesterday_price*1000
      ydvalue = [(float(data_list[1][i+1])*float(data_list[3][i+1])*1000) for i in range(len(data_list[0])-1)]
    csvfile.close()      
def main():
  aa = Myaccount("account.csv")
  aa.somevalue()
if __name__ == '__main__':
  main()



