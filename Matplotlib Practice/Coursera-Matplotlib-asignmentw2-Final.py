import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import os
os.chdir('/Users/alex/Downloads')

cname = "fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv"
df = pd.read_csv(cname)
df['Data_Value']=df['Data_Value']/10
df['Date'] = pd.to_datetime(df['Date'],format='%Y-%m-%d')
print(df.head())


#temp min & max for each day
dfmax = df[df['Element']=='TMAX'].groupby('Date')['Data_Value'].max()
dfmin = df[df['Element']=='TMIN'].groupby('Date')['Data_Value'].min()

#temp min & max per calendar day
df2 = dfmax.to_frame('TMax')
df2['TMin'] = dfmin
df2['md']=df2.index.strftime('%m%d')
df3 = df2[(df2.index<=pd.to_datetime('2014-12-31')) & (df2['md']!='0229')]
df3 = df3.groupby('md').agg({'TMin':'min','TMax':'max'})

df4 = df2[df2.index>pd.to_datetime('2014-12-31')].reset_index().set_index('md')
df5 = df4[df4['TMax']>=df3['TMax']]
df6 = df4[df4['TMin']<=df3['TMin']]


plt.figure()
plt.plot(df4['Date'],df3['TMin'], 'r-',df4['Date'],df3['TMax'], 'b-',linewidth = 0.5)
plt.scatter(df5['Date'],df5['TMax'],s = 5, c='darkblue')
plt.scatter(df6['Date'],df6['TMin'],s = 5, c='darkred')

plt.gca().fill_between(df4['Date'],df3['TMin'],df3['TMax'] ,facecolor='gainsboro')

plt.legend(['Max 2005-2014', 'Min 2005-2014', '2015 above Max', '2015 below Min'], loc=8, frameon=False)

ax = plt.gca()
#for spine in ax.spines.values(): spine.set_visible(False)
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_title('Interval of min-max temperatures for 2005-2014 near Ann Arbor, Michigan, United States \n and temperatures of 2015, dropping out of the interval')
ax.set_ylabel('Temperature, °C', fontsize = 15, labelpad = 20)
#ax.yaxis.set_tick_params(labelsize=7)


x = ax.xaxis
for item in x.get_ticklabels():
    item.set_rotation(45)
x.set_major_locator(mdates.MonthLocator(interval=1))
#x.set_major_formatter(mdates.DateFormatter('%Y-%m'))
x.set_major_formatter(mdates.DateFormatter('%b'))
#plt.subplots_adjust(bottom=0.25)
#plt.xlim(xmin=pd.to_datetime('2005-01-01'),xmax=pd.to_datetime('2015-12-31'))
plt.xlim(xmin=pd.to_datetime('2015-01-01'),xmax=pd.to_datetime('2015-12-31'))

plt.show()

