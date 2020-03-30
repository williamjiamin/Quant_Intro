#import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
#from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from candlestick import william_edu_candlestick


#Get data and adjust display option

style.use('ggplot')
pd.set_option('display.max_columns',None)
pd.set_option('display.max_row',None)

#df= ts.get_hist_data('000001')
#print(df.head())

#Save data to csv files and read from csv files
#df.to_csv('000001.csv')
df_read_from_csv=pd.read_csv('000001.csv',parse_dates=True,index_col=0)
df_read_from_csv_reverse_order=df_read_from_csv.sort_index(ascending=True)
#print(df_read_from_csv_reverse_order.head())

#Use pandas to plot data
#df_read_from_csv[['open','close']].plot()
#print(df_read_from_csv['close'])
#plt.show()


#Customized 7 days moving average
df_read_from_csv_reverse_order['ma7']=df_read_from_csv_reverse_order['close'].rolling(window=7).mean()
#print(df_read_from_csv_reverse_order.head())
df_read_from_csv_reverse_order.dropna(inplace=True)
#df_read_from_csv_reverse_order['ma7'].plot()
#plt.show()


#Using matplotlib.pyplot to draw subplot
ax1= plt.subplot2grid((9,10),(0,0),rowspan=7,colspan=10)
ax2= plt.subplot2grid((9,10),(7,0),rowspan=2,colspan=10,sharex=ax1)
ax1.xaxis_date()

#print(df_read_from_csv_reverse_order.head())
#ax1.plot(df_read_from_csv_reverse_order.index,
#         df_read_from_csv_reverse_order['close'])
#ax1.plot(df_read_from_csv_reverse_order.index,
#         df_read_from_csv_reverse_order['ma7'])
#ax2.bar(df_read_from_csv_reverse_order.index,
#         df_read_from_csv_reverse_order['volume'])
#
#plt.show()

#Using matplotlib to draw candlestick
df_ohlc=df_read_from_csv_reverse_order[['open','close','high','low']]
df_ohlc=df_ohlc.reset_index()
df_ohlc['date']=df_ohlc['date'].map(mdates.date2num)
#print(df_ohlc.head())

william_edu_candlestick(ax1,df_ohlc.values,width=1,colordown='green',
                        colorup='red',alpha=0.75)
ax2.bar(df_read_from_csv_reverse_order.index,
         df_read_from_csv_reverse_order['volume'])

plt.show()















