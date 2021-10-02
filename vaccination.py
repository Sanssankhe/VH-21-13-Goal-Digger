import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator
from datetime import timedelta

df = pd.read_csv(
    'https://covid.ourworldindata.org/data/owid-covid-data.csv', 
    usecols=['date', 'location', 'total_vaccinations_per_hundred'], 
    parse_dates=['date'])

countries = ['India', 'Germany', 'United Kingdom', 'Israel']
df = df[df['location'].isin(countries)]

pivot = pd.pivot_table(
    data=df,                                    
    index='date',                               
    columns='location',                         
    values='total_vaccinations_per_hundred',    
    aggfunc='mean',                             
    )

pivot = pivot.fillna(method='ffill')

main_country = 'India'
colors = {country:('grey' if country!= main_country else '#129583') for country in countries}
alphas = {country:(0.75 if country!= main_country else 1.0) for country in countries}

fig, ax = plt.subplots(figsize=(12,8))
fig.patch.set_facecolor('#F5F5F5')    
ax.patch.set_facecolor('#F5F5F5')     

for country in countries:
    ax.plot(
        pivot.index,           
        pivot[country],           
        color=colors[country],    
        alpha=alphas[country]     
    )
    ax.text(
        x = pivot.index[-1] + timedelta(days=2),  
        y = pivot[country].max(),                   
        color = colors[country],                    
        s = country,                                
        alpha=alphas[country]                     
    )

date_form = DateFormatter("%Y-%m-%d")
ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(0), interval=1))
ax.xaxis.set_major_formatter(date_form)
plt.xticks(rotation=45)
plt.ylim(0,100)


ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#3f3f3f')
ax.spines['left'].set_color('#3f3f3f')
ax.tick_params(colors='#3f3f3f')
ax.grid(alpha=0.1)


plt.ylabel('Total Vaccinations per 100 People', fontsize=12, alpha=0.9)
plt.xlabel('Date', fontsize=12, alpha=0.9)
plt.title('COVID-19 Vaccinations over Time', fontsize=18, weight='bold', alpha=0.9)


plt.show()

