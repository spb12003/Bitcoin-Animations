import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from itertools import count
from matplotlib.animation import FuncAnimation
from datetime import datetime
from matplotlib.patches import Rectangle


btc = 'BTC/USD'
msft = "MSFT"
gold = "GLD"
sp_500 = 'SPX'
real_estate = 'VNQ'
forn_cur1 = 'TRY/USD'  ##Turkish Lira
forn_cur2 = 'VEF/USD'   ##Venezuelan Bolivar

api_key = "aee10077fe41414e81d610a6340290a4"
time = '1week'
cur_date = datetime.now()
cur_date_form = cur_date.strftime('%Y-%m-%d')


## try to make this a template function for 
def get_data(symbol, end_date, interval, api):
    api_url = f'https://api.twelvedata.com/time_series?symbol={symbol}&start_date=2013-11-22&end_date={end_date}&interval={interval}&apikey={api}'
    response = requests.get(api_url).json()
    data = pd.DataFrame(response['values'])
    data = data.iloc[::-1].reset_index(drop=True)  # This line reverses the DataFrame.
    return data



#This data is in the right order for use
msft_data = get_data(msft, cur_date_form, time, api_key)
btc_data = get_data(btc, cur_date_form, time, api_key)
btc_data.to_csv("data.csv", index=False)
sp_data = get_data(sp_500, cur_date_form, time, api_key)
gold_data = get_data(gold, cur_date_form, time, api_key).drop_duplicates(subset='datetime', keep='first').reset_index(drop=True)  ##gold data had duplicates so this line deletes them but keeps the first
re_data = get_data(real_estate, cur_date_form, time, api_key).drop_duplicates(subset='datetime', keep='first').reset_index(drop=True)
cur1_data = get_data(forn_cur1, cur_date_form, time, api_key)

#convert to float type
btc_data['open'] = btc_data['open'].astype(float)
msft_data['open'] = msft_data['open'].astype(float)
sp_data['open'] = sp_data['open'].astype(float)
gold_data['open'] = gold_data['open'].astype(float)
re_data['open'] = re_data['open'].astype(float)
cur1_data['open'] = cur1_data['open'].astype(float)

#normalize the 1st data point to 100% if needed
base_btc = btc_data.iloc[0, 1]
base_msft = msft_data.iloc[0, 1]
base_sp = sp_data.iloc[0, 1]
base_gold = gold_data.iloc[0, 1]
base_re = re_data.iloc[0, 1]
base_cur1 = cur1_data.iloc[0, 1]

#calc a ratio if needed
ratio_msft = base_btc / base_msft
ratio_sp = base_btc / base_sp
ratio_gold = base_btc / base_gold
ratio_re = base_btc / base_re
ratio_cur1 = base_btc / base_cur1


#create a new column in the data sets
btc_data['percentage'] = (btc_data['open'] / btc_data['open']) * 100
btc_data['usd percent'] = (base_btc / btc_data['open']) * 100
msft_data['percentage'] = (ratio_msft * msft_data['open'] / btc_data['open']) * 100
sp_data['percentage'] = (ratio_sp * sp_data['open'] / btc_data['open']) * 100
gold_data['percentage'] = (ratio_gold * gold_data['open'] / btc_data['open']) * 100
re_data['percentage'] = (ratio_re * re_data['open'] / btc_data['open']) * 100
cur1_data['percentage'] = (ratio_cur1 * cur1_data['open'] / btc_data['open']) * 100

#convert to float type
btc_data['percentage'] = btc_data['percentage'].astype(float)
msft_data['percentage'] = msft_data['percentage'].astype(float)
sp_data['percentage'] = sp_data['percentage'].astype(float)
gold_data['percentage'] = gold_data['percentage'].astype(float)
re_data['percentage'] = re_data['percentage'].astype(float)
cur1_data['percentage'] = cur1_data['percentage'].astype(float)


plt.style.use('dark_background')

#empty variable for each data set
x = []
y = []

x_msft = []
y_msft = []

x_usd = []
y_usd = []

x_sp = []
y_sp = []

x_re = []
y_re = []

x_cur1 = []
y_cur1 = []

x_gold = []
y_gold = []


#reformat the dates to be more readable
def reformat_date(date_string):
    # Parse the string into a datetime object
    dt = datetime.strptime(date_string, '%Y-%m-%d')
    # Format the datetime object into your desired string format
    return dt.strftime('%B %d, %Y')

fig, ax = plt.subplots()
fig.subplots_adjust(left=0.2, top=0.75, bottom= 0.2, right=0.9)


#counter to iterate thru csv
counter=count(0,1)

#function to use in FuncAnimation()
def update(i):

    idx=next(counter)
    #use the reformat_date() function to change the 
    formatted_date = reformat_date(btc_data.iloc[idx, 0])
    x.append(formatted_date)
    y.append(float(btc_data.iloc[idx, 5]))

    x_msft.append(formatted_date)
    y_msft.append(float(msft_data.iloc[idx, 6]))

    x_usd.append(formatted_date)
    y_usd.append(float(btc_data.iloc[idx, 6]))

    x_sp.append(formatted_date)
    y_sp.append(float(sp_data.iloc[idx, 6]))

    x_gold.append(formatted_date)
    y_gold.append(float(gold_data.iloc[idx, 6]))

    x_re.append(formatted_date)
    y_re.append(float(re_data.iloc[idx, 6]))

    x_cur1.append(formatted_date)
    y_cur1.append(float(cur1_data.iloc[idx, 5]))
    

    plt.cla()
    
    ax.set_yscale("log")
    ax.set_ylim(0.1, 10)
    ax.set_yticks([0.1, 1.0, 10, 100, 1000])
    ax.yaxis.set_major_formatter('{:,.0f}%'.format)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    y_value_btc = y[-1]
    label_text_btc = f"Bitcoin {y_value_btc:,.1f}%"

    y_value_msft = y_msft[-1]
    label_text_msft = f"MSFT Stock {y_value_msft:,.2f}%"

    y_value_usd = y_usd[-1]
    label_text_usd = f"US Dollar {y_value_usd:,.2f}%"

    y_value_sp = y_sp[-1]
    label_text_sp = f"S&P 500 {y_value_sp:,.2f}%"

    y_value_gold = y_gold[-1]
    label_text_gold = f"Gold {y_value_gold:,.2f}%"

    y_value_re = y_re[-1]
    label_text_re = f"Real Estate {y_value_re:,.2f}%"

    y_value_cur1 = y_cur1[-1]
    label_text_cur1 = f"Turkish Lira {y_value_cur1:,.2f}%"


    #print(y)
    ax.plot(x, y, color='orange', label='Bitcoin')
    ax.text(x[-1], y[-1], label_text_btc, color='orange', verticalalignment='center', fontsize=5)
    ax.plot(x_msft, y_msft, color='cyan', label='Microsoft')
    ax.text(x_msft[-1], y_msft[-1], label_text_msft, color='cyan', verticalalignment='center', fontsize=5)
    ax.plot(x_usd, y_usd, color='lime', label='USD')
    ax.text(x_usd[-1], y_usd[-1], label_text_usd, color='lime', verticalalignment='bottom', fontsize=5)
    ax.plot(x_sp, y_sp, color='lightsteelblue', label='S&P 500')
    ax.text(x_sp[-1], y_sp[-1], label_text_sp, color='lightsteelblue', verticalalignment='center', fontsize=5)
    ax.plot(x_gold, y_gold, color='gold', label='Gold')
    ax.text(x_gold[-1], y_gold[-1], label_text_gold, color='gold', verticalalignment='center', fontsize=5)
    ax.plot(x_re, y_re, color='white', label='Real Estate')
    ax.text(x_re[-1], y_re[-1], label_text_re, color='white', verticalalignment='top', fontsize=5)
    #ax.plot(x_cur2, y_cur2, color='red', label='Gold')
    ax.plot(x_cur1, y_cur1, color='pink', label='Turkish Lira')
    ax.text(x_cur1[-1], y_cur1[-1], label_text_cur1, color='pink', verticalalignment='center', fontsize=5)

    plt.title('Bitcoin as a Store of Value', fontsize=22.5)
    plt.xlabel('Date', fontsize=12.5)
    plt.ylabel('Percent', fontsize=12.5)
    
    # Declutter the x-axis
    if len(x) > 1:
        x_ticks = [x[0], x[int(len(x)*0.25)], x[int(len(x)*0.5)], x[int(len(x)*0.75)], x[-1]]
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_ticks, rotation=20, ha='right', fontsize=7.5)
       
    else:
        ax.set_xticks([x[0]])


max_frames= len(btc_data)
ani=FuncAnimation(fig=fig, func=update, frames=max_frames, interval=20)

plt.show()