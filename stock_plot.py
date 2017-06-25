import matplotlib.pyplot as plt 
import numpy as np 
#from matplotlib import font_manager
class Plot:
  def __init__(self,date,stock_number,plot_kind,stock_name):
    self.stock_number = stock_number
    self.plot_kind = plot_kind
    self.stock_name = stock_name
    self.date = date

  def histprice_plot(self,hist_price,amplitude):
    #fontP = font_manager.FontProperties()
    plt.figure(figsize=(12,5))
    x = np.arange(len(self.date))
    plt.subplot(2,1,1)
    plt.xticks(x,self.date)
    plt.xlabel('day')
    plt.ylabel('price')
    plt.title(self.stock_number+' '+ self.plot_kind)
    plt.plot(x,hist_price,'ro')

    #plt.xticks(x,self.date)
    #plt.xlabel('day')
    #plt.ylabel('price')
    #plt.title(self.stock_number+' '+ self.plot_kind)
    #plt.plot(x,hist_price,'ro')
    #amplitude = tuple(amplitude)
    amplituder = []
    amplitudeg = []
    for i in range(len(amplitude)):
      if(amplitude[i]>=0):
        amplituder.append(amplitude[i])
        amplitudeg.append(0)
      else:
        amplituder.append(0)
        amplitudeg.append(amplitude[i])
    plt.subplot(2,1,2)
    plt.xticks(x,self.date)
    plt.xlabel('day')
    plt.ylabel('amplitude(%)')
    plt.ylim(-10,10)
    plt.bar(x,tuple(amplituder),width = 0.35,color='r')
    plt.bar(x,tuple(amplitudeg),width = 0.35,color='g')
    plt.savefig(self.stock_name+'_'+self.plot_kind+'.png')
  def MACDPlot(self,DIF,DEM):
    x = np.arange(79)
    plt.ylim(-5,5)
    plt.plot(x,DIF,'r')
    plt.plot(x,DEM,'g')
    plt.show()

