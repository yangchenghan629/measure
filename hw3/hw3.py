import csv as csv
import numpy as np
import matplotlib.pyplot as plt , matplotlib.dates as mdates
import datetime as datetime
import pandas as pd

def smooth(x,w):
    return pd.DataFrame.rolling(pd.DataFrame(x),window=w,center=True).mean()

path_list=['./466920Taipei-2025-RelativeHumidity-month.csv',
           './467080Yilan-2025-RelativeHumidity-month.csv',
           './467410Tainan-2025-RelativeHumidity-month.csv',
           './467490Taichung-2025-RelativeHumidity-month.csv',
           './467660Taitung-2025-RelativeHumidity-month.csv']

stationname=['Taipei','Yilan','Tainan','Taichung','Taitung']

year=[30,11,29,30,45]
gap=[0,20,0,0,20]

rh=np.full((101,12,len(path_list)),np.nan)
kstation=0

for path in path_list:
    file=open(path)
    var=list(csv.reader(file,delimiter=','))
    for irow in range(year[kstation],len(var)-3+1):
        for jcol in range(1,13):
            if str(var[irow][jcol])=='--'or str(var[irow][jcol])=='x':
                rh[irow-year[kstation]+gap[kstation],jcol-1,kstation]=np.nan
            else:
                rh[irow-year[kstation]+gap[kstation],jcol-1,kstation]=float(var[irow][jcol])
    kstation+=1

climate=np.nanmean(rh,axis=0)
climate_repeat=np.tile(climate,(101,1))
rh=np.reshape(rh,(101*12,5))
anomaly=rh-climate_repeat


time=[]
for y in range(1924,2025):
    for m in range(1,13):
        time.append(datetime.datetime(y,m,1))


# fig=plt.figure(figsize=(10,8))
# plt.suptitle('Monthly Relative Humidity and 10-year Smoothing',fontsize=18)
# for i in range(5):
#     ax=fig.add_subplot(2,3,i+1)
#     plt.title(stationname[i],fontsize=14)
#     if i==0:
#         plt.plot(time,rh[:,i],'b',label='Monthly RH')
#         plt.plot(time,smooth(rh[:,i],120),'r',label='10-year Smoothing')
#     else:
#         plt.plot(time,rh[:,i],'b')
#         plt.plot(time,smooth(rh[:,i],120),'r')
#     plt.grid()
#     ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
#     ax.xaxis.set_major_locator(mdates.YearLocator(20))
#     plt.xticks(rotation=45)
#     plt.xlim([datetime.datetime(1920,1,1),datetime.datetime(2030,1,1)])
#     plt.ylim([60,100])
#     plt.xlabel('Time',fontsize=12)
#     plt.ylabel('RH [%]',fontsize=12)
# fig.legend(loc=(0.7,0.2),fontsize=12)
# plt.tight_layout()
# plt.savefig('rh.png',dpi=450)

# plt.clf()
# plt.figure(figsize=(8,5))
# plt.title('10-year Smoothing of Monthly Relative Humidity',fontsize=14)
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
# plt.gca().xaxis.set_major_locator(mdates.YearLocator(10))
# for i in range(5):
#     plt.plot(time,smooth(rh[:,i],120),label=stationname[i],linewidth=1.5)
# plt.legend(fontsize=10)
# plt.xlim([datetime.datetime(1920,1,1),datetime.datetime(2025,1,1)])
# plt.ylim([70,90])
# plt.xlabel('Time',fontsize=12)
# plt.ylabel('RH [%]',fontsize=12)
# plt.grid()
# plt.savefig('smooth.png')


# fig=plt.figure(figsize=(10,8))
# plt.suptitle('Monthly Relative Humidity Anomaly and 10-year Smoothing',fontsize=18)
# for i in range(5):
#     ax=fig.add_subplot(2,3,i+1)
#     plt.title(stationname[i],fontsize=14)
#     if i==0:
#         plt.plot(time,anomaly[:,i],'b',label='Monthly Anomaly')
#         plt.plot(time,smooth(anomaly[:,i],120),'r',label='10-year Smoothing')
#     else:
#         plt.plot(time,anomaly[:,i],'b')
#         plt.plot(time,smooth(anomaly[:,i],120),'r')
#     plt.hlines(0,xmin=datetime.datetime(1920,1,1),xmax=datetime.datetime(2030,1,1),colors='k')
#     plt.grid()
#     ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
#     ax.xaxis.set_major_locator(mdates.YearLocator(20))
#     plt.xticks(rotation=45)
#     plt.xlim([datetime.datetime(1920,1,1),datetime.datetime(2030,1,1)])
#     plt.ylim([-20,20])
#     plt.xlabel('Time',fontsize=12)
#     plt.ylabel('Anomaly',fontsize=12)
# fig.legend(loc=(0.7,0.2),fontsize=12)
# plt.tight_layout()
# plt.savefig('anomaly.png',dpi=450)


# plt.clf()
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
# plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
# for k in range(0,5):
#     plt.plot([datetime.datetime(2000,i,1) for i in range(1,13)],climate[:,k],'-',label=stationname[k])
# plt.xlim([datetime.datetime(2000,1,1),datetime.datetime(2000,12,1)])
# plt.ylim([70,90])
# plt.grid()
# plt.xlabel('Month')
# plt.ylabel('RH [%]')
# plt.title('100-year RH Climate Value')
# plt.legend(bbox_to_anchor=(0.45,-0.17),ncol=5,loc='center')
# plt.savefig('climate.png',bbox_inches='tight')

plt.clf()
plt.plot(time,rh[:,0],'b-o')
plt.xlim(datetime.datetime(1960,1,1),datetime.datetime(1960,12,1))
plt.xticks(rotation=45)
plt.grid()
plt.savefig('a_year.png',bbox_inches='tight')