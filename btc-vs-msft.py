import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from itertools import count
from matplotlib.animation import FuncAnimation
from datetime import datetime
from matplotlib.patches import Rectangle



msft = "MSFT"
btc = 'BTC/USD'
api_key = "aee10077fe41414e81d610a6340290a4"
interval = '1week'

cur_date = datetime.now()
cur_date_form = cur_date.strftime('%Y-%m-%d')

api_url_btc = f'https://api.twelvedata.com/time_series?symbol={btc}&start_date=2014-08-31&end_date={cur_date_form}&interval={interval}&apikey={api_key}'


data_json = requests.get(api_url_btc).json()
data = pd.DataFrame(data_json['values'])
data = data.iloc[::-1].reset_index(drop=True)  # This line reverses the DataFrame.


api_url_msft = f'https://api.twelvedata.com/time_series?symbol={msft}&start_date=2014-08-31&end_date={cur_date_form}&interval={interval}&apikey={api_key}'
data_json2 = requests.get(api_url_msft).json()
data2 = pd.DataFrame(data_json2['values'])
data2 = data2.iloc[::-1].reset_index(drop=True)  # This line reverses the DataFrame.


plt.style.use('dark_background')

x = []
y = []

x_msft = []
y_msft = []


#reformat the dates to be more readable
def reformat_date(date_string):
    # Parse the string into a datetime object
    dt = datetime.strptime(date_string, '%Y-%m-%d')
    
    # Format the datetime object into your desired string format
    return dt.strftime('%B %d, %Y')


fig, ax = plt.subplots()
#ax.plot(x, y)
fig.subplots_adjust(left=0.2, top=0.75, bottom= 0.2, right=0.9)



date_bg = Rectangle((0.05, 0.85), width=0.3, height=0.11, transform=fig.transFigure, color='silver', alpha=0.7)
price_bg = Rectangle((0.69, 0.85), width=0.3, height=0.11, transform=fig.transFigure, color='silver', alpha=0.7)
fig.patches.extend([date_bg, price_bg])

wrd_date_text = fig.text(0.07, 0.945, 'Date:', color='black', verticalalignment='top', fontsize=14)
wrd_price_text = fig.text(0.71, 0.945, 'BTC Price:', color='black', verticalalignment='top', fontsize=14)

date_text = fig.text(0.07, 0.895, '', color='black', verticalalignment='top', fontsize=12.5)
price_text = fig.text(0.71, 0.895, '', color='black', verticalalignment='top', fontsize=12.5)


#counter to iterate thru csv
counter=count(0,1)

#function to use in FuncAnimation()
def update(i):

    
    idx=next(counter)
    #use the reformat_date() function to change the 
    formatted_date = reformat_date(data.iloc[idx, 0])
    x.append(formatted_date)
    y.append(float(data.iloc[idx, 1]))

    y_msft.append(float(data2.iloc[idx, 1]))
    x_msft.append(formatted_date)

    plt.cla()
    
    ax.plot(x, y, color='orange')
    ax.plot(x_msft, y_msft, color='blue', label='Microsoft')


    plt.title('Bitcoin Vs Microsoft', fontsize=22.5)
    plt.xlabel('Date', fontsize=12.5)
    plt.ylabel('Price (USD)', fontsize=12.5)
    ax.yaxis.set_major_formatter('${:,.0f}'.format)

    # Declutter the x-axis
    if len(x) > 1:
        x_ticks = [x[0], x[int(len(x)*0.25)], x[int(len(x)*0.5)], x[int(len(x)*0.75)], x[-1]]
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_ticks, rotation=20, ha='right', fontsize=7.5)
       
    else:
        ax.set_xticks([x[0]])


    date_text.set_text(f'{x[-1]}')
    price_text.set_text(f'${y[-1]:,.2f}')    
    

max_frames= len(data)
ani=FuncAnimation(fig=fig, func=update, frames=max_frames, interval=20)

plt.show()
