from stockinfo import Stockinfo
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("-f","--Filename",type=str,help="Input the name of file which contains the stock numbers")
parser.add_argument("-i","--Implementtype",type=str,help = "Input the type of function you want to implement")
args = parser.parse_args()

sto_pro = Stockinfo(args.Filename,args.Implementtype)
sto_pro.readfile()
sto_pro.getweburl()
sto_pro.daily_price()
