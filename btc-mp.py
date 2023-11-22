import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from itertools import count
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter





api_url = f'https://data.nasdaq.com/api/v3/datasets/BCHAIN/TOTBC.json?api_key=qybJvvJ1fsWnyCqRZgCS'
response = requests.get(api_url).json()
data = pd.DataFrame(response['dataset']['data'])
data = data.iloc[::-1].reset_index(drop=True)  # This line reverses the DataFrame.


# Rename columns for clarity
data.columns = ['Date', 'Cumulative_Supply']
# Calculate the daily increase in supply
data['Daily_Increase'] = data['Cumulative_Supply'].diff()
# Handle the first day (which will have NaN after diff())
data['Daily_Increase'].iloc[0] = 0
# Calculate the annualized inflation rate
data['infl_rate'] = (data['Daily_Increase'] / data['Cumulative_Supply']) * 365 * 100
data = data[data['infl_rate'] > 0]


#Start making the graphic
plt.style.use('dark_background')

#empty variable for each data set
x_btc_supply = []
y_btc_supply = []

x_infl_rate = []
y_infl_rate = []


#reformat the dates to be more readable
def reformat_date(date_string):
    # Parse the string into a datetime object
    dt = datetime.strptime(date_string, '%Y-%m-%d')
    
    # Format the datetime object into your desired string format
    return dt   ##.strftime('%B %d, %Y')


#create function to calc btc supply per day
def total_supply(days):
    reward = 50.0
    days_per_halving = 1458
    total_btc = 0
    supply = []
    
    while days > 0:
        blocks_this_period = min(days, days_per_halving)
       
        for _ in range(blocks_this_period):
            total_btc += reward * (24 * 6)
            #print(total_btc)
            supply.append(total_btc)
           # print(supply)
        days -= blocks_this_period
        reward /= 2
    
    return supply

#Create function to calculate the annualized inflation rate per day
def inflation_rate(days):
    reward = 50.0
    days_per_halving = 1458
    total_btc = 0
    infl_rate = []
    
    while days > 0:
        blocks_this_period = min(days, days_per_halving)
       
        for _ in range(blocks_this_period):
            daily_btc = reward * (24 * 6)
            #print(daily_btc)
            total_btc += reward * (24 * 6)
            daily_rate = daily_btc * 365 / total_btc * 100
            #print(daily_rate)
            infl_rate.append(daily_rate)
            #print(infl_rate)

        days -= blocks_this_period
        reward /= 2
    
    return infl_rate


# Define a range of blocks
num_days = 10000
days = [datetime(2009, 1, 3) + timedelta(days=i) for i in range(num_days)]

# Get the total supply for each block
supply = total_supply(num_days)
#print(supply)

inflation = inflation_rate(num_days)

fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot total supply on the primary y-axis
color = 'tab:blue'
ax1.set_xlabel("Time")
ax1.set_ylabel("Total Supply (BTC)", color=color)
ax1.plot(days, supply, label="Bitcoin Supply", color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))

# Create a secondary y-axis for the inflation rate
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Annualized Inflation Rate (%)', color=color)
ax2.plot(days, inflation, label="Annualized Inflation Rate", color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_yscale("log")
ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: '{:,.2f}'.format(x)))

ax1.grid(False)
ax2.grid(False)
fig.tight_layout()
plt.title("Bitcoin Monetary Policy")
plt.tight_layout()

#counter to iterate 
counter=count(0,25)
def update(i):
    
    idx=next(counter)
    #use the reformat_date() function to change the 
    formatted_date = reformat_date(data.iloc[idx, 0])
    x_btc_supply.append(formatted_date)
    y_btc_supply.append(float(data.iloc[idx, 1]))

    x_infl_rate.append(formatted_date)
    y_infl_rate.append(float(data.iloc[idx, 3]))

    ax1.plot(x_btc_supply, y_btc_supply, color='orange')
    ax2.plot(x_infl_rate, y_infl_rate, color='green')

    # Declutter the x-axis
    if len(x_btc_supply) > 1:
        x_ticks = [x_btc_supply[0], x_btc_supply[int(len(x_btc_supply)*0.25)], x_btc_supply[int(len(x_btc_supply)*0.5)], x_btc_supply[int(len(x_btc_supply)*0.75)], x_btc_supply[-1]]
        ax1.set_xticks(x_ticks)
        ax1.set_xticklabels(x_ticks, rotation=20, ha='right', fontsize=7.5)
       
    else:
        ax1.set_xticks([x_btc_supply[0]])   
    

max_frames= len(data)
ani=FuncAnimation(fig=fig, func=update, frames=max_frames, interval=100)

plt.show()

















