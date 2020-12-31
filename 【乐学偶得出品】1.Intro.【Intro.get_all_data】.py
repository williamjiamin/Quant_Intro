# 乐学偶得版权所有 lexueoude.com 公众号1：乐学Fintech 2: 乐学偶得
import bs4 as bs
import pickle
import tushare as ts
import os
import pandas as pd 
import numpy as np
import  matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')


#
#ts.set_token('')
#pro=ts.pro_api()
#df=pro.daily(ts_code='000001.SZ',start_date='20180101',end_date='20181118')
#print(df)

#History CSI 300
def find_and_save_CSI_300():
    response = requests.get('https://en.wikipedia.org/wiki/CSI_300_Index')
    soup = bs.BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker[:6]
        tickers.append(ticker)
        
    with open("CSI_tickers.pickle","wb") as f:
        pickle.dump(tickers,f)
    print(tickers)
    return tickers

#find_and_save_CSI_300()

#Find and Save Latest CSI 300 and make it compatible with tushare pro API
def find_and_save_CSI_300():
    CSI_300_df=ts.get_hs300s()
    tickers=CSI_300_df['code'].values
#    print(tickers)
    tickers_mod=[]
    for ticker in tickers:
        if ticker[0] == '6':
            ticker=ticker+'.SH'
            tickers_mod.append(ticker)
        else:
            ticker=ticker+'.SZ'
            tickers_mod.append(ticker)
    print(tickers_mod)

    with open("CSI_tickers.pickle","wb") as f:
        pickle.dump(tickers_mod,f)
    print(tickers_mod)
    return tickers_mod
           
#find_and_save_CSI_300()
    

#Use CSI 300 list to get data from tushare pro API

def get_data_from_tushare(reload_CSI_300=False):
    if reload_CSI_300:
        tickers_mod=find_and_save_CSI_300()
    else:
        with open("CSI_tickers.pickle","rb") as f:
            tickers_mod=pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    for ticker_mod in tickers_mod:
        print(ticker_mod)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker_mod)):
            df=pro.daily(ts_code=str(ticker_mod),
                         start_date='20160101',end_date='20181118')
            df.reset_index(inplace=True)
            df.set_index('trade_date',inplace=True)
            df.to_csv('stock_dfs/{}.csv'.format(ticker_mod))
        else:
            print('Hey~~~We already have {}'.format(ticker_mod))

#get_data_from_tushare()

#Put all stock close price into one dataframe

def put_all_stock_price_into_one_df():
    with open("CSI_tickers.pickle","rb") as f:
        tickers=pickle.load(f)
    all_stock_price_df=pd.DataFrame()
#    print(all_stock_price_df)
    for count , ticker in enumerate(tickers):
        df=pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('trade_date',inplace=True)
        
        df.rename(columns={'close':ticker},inplace=True)
        df.drop(['index','ts_code','open','high','low','pre_close',
                 'change','pct_chg','vol','amount'],1,inplace=True)
        
        if all_stock_price_df.empty:
            all_stock_price_df=df
        else:
            all_stock_price_df=all_stock_price_df.join(df,how='outer')
        print(count)
#    print(all_stock_price_df.head())
    all_stock_price_df.to_csv('CSI_300_Joined_closes.csv')

#put_all_stock_price_into_one_df()
            

#Calculate ,save and Plot pearson correlation heatmap

def calculate_save_and_plot_pearson_correlation_heatmap():
    df = pd.read_csv('CSI_300_Joined_closes.csv')
    df_corr = df.pct_change().corr()
#    print(df_corr.head())
#    df_corr.to_csv('CSI_300_pct_change_corr.csv')
    data=df_corr.values  
    
#    print(data.shape)
    
    fig=plt.figure()
    ax=fig.add_subplot(111)
    
    heatmap=ax.pcolor(data,cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    
    ax.set_xticks(np.arange(0.5,data.shape[0]+0.5,step=1),minor=False)
    ax.set_yticks(np.arange(0.5,data.shape[1]+0.5,step=1),minor=False)
    
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    
    column_labels=df_corr.columns
    row_labels=df_corr.index


    ax.set_xticklabels(column_labels) 
    ax.set_yticklabels(row_labels)
    
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)
    plt.tight_layout()
    plt.show()

calculate_save_and_plot_pearson_correlation_heatmap()
    




        
        
    

































