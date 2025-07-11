# IMPORT MODULES
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt , matplotlib.dates as mdates , matplotlib.cm as cm
import datetime as datetime
import windrose as wr

def smooth(x,w):
    return pd.DataFrame.rolling(pd.DataFrame(x),window=w,center=True).mean()

# READ DATA
####################################################
time=pd.read_excel('20111120-20111126-NTU_AS weather.xls',usecols=[0],converters={'COLUMN':pd.to_datetime})
temp=pd.DataFrame.to_numpy(pd.read_excel('20111120-20111126-NTU_AS weather.xls',usecols=[5]))[:,0]
pres=pd.DataFrame.to_numpy(pd.read_excel('20111120-20111126-NTU_AS weather.xls',usecols=[1]))[:,0]
rh=pd.DataFrame.to_numpy(pd.read_excel('20111120-20111126-NTU_AS weather.xls',usecols=[3]))[:,0]
wd=pd.DataFrame.to_numpy(pd.read_excel('20111120-20111126-NTU_AS weather.xls',usecols=[6]))[:,0]
ws=pd.DataFrame.to_numpy(pd.read_excel('20111120-20111126-NTU_AS weather.xls',usecols=[7]))[:,0]


# CALCULATION
###################################################
# daily max/min/mean temperature
daily_temp=temp.copy().reshape((7,len(temp)//7))
daily_mean_temp=np.mean(daily_temp,axis=0)
max_temp_loc=np.argmax(daily_temp,axis=1)
min_temp_loc=np.argmin(daily_temp,axis=1)
mean_temp=np.mean(daily_temp,axis=1)
for i in range(7):
    max_temp_loc[i]+=1440*i
    min_temp_loc[i]+=1440*i

# vapor pressure | dew point | specific humidity
A=7.5
B=237.3
epsilon=0.622
es=6.1078*10**((temp*A)/(temp+B))
e=rh*es/100
td=(B*np.log10(e/6.1078)/(A-np.log10(e/6.1078)))
qv=epsilon*e/(pres-(1-epsilon)*e)
daily_rh_mean=np.mean(rh.copy().reshape((7,len(rh)//7)),axis=0)
daily_es_mean=np.mean(es.copy().reshape((7,len(es)//7)),axis=0)
daily_e_mean=np.mean(e.copy().reshape((7,len(e)//7)),axis=0)

# wdws->uv | 10-min average wind
angle=wd*np.pi/180
u=-ws*np.sin(angle)
v=-ws*np.cos(angle)
u=u.reshape((10,len(u)//10))
v=v.reshape((10,len(v)//10))
u10=np.mean(u,axis=0)
v10=np.mean(v,axis=0)
ws10=(u10**2+v10**2)**0.5
wd10 = (np.degrees(np.arctan2(-u10, -v10)) + 360) % 360

# mean wind speed
daily_ws_mean=np.mean(ws.copy().reshape((7,len(ws)//7)),axis=0)

# GRAPHING
###################################################
# temperature time series
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.title('Temperature',fontweight='bold',fontsize=14)
plt.xticks(rotation=45)
plt.plot(time,temp)
plt.scatter(time.iloc[max_temp_loc],temp[max_temp_loc],c=['r'],)
plt.scatter(time.iloc[min_temp_loc],temp[min_temp_loc],c=['r'])
for i in range(7):
    plt.text(time.iloc[max_temp_loc[i]],temp[max_temp_loc[i]]+0.05,f'{temp[max_temp_loc[i]]:02.1f}')
    plt.text(time.iloc[min_temp_loc[i]],temp[min_temp_loc[i]],f'{temp[min_temp_loc[i]]:02.1f}')
plt.grid()
plt.xlim(datetime.datetime(2011,11,19,23,59),datetime.datetime(2011,11,27,00,1))
plt.xlabel('Time',fontsize=12)
plt.ylabel('Temperature[K]',fontsize=12)
plt.savefig('Temp.png',dpi=450)
plt.clf()

# Maximum/Minimum and Mean Temperature
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.plot([datetime.datetime(2011,11,d) for d in range(20,27)],temp[max_temp_loc],'r-o',label='max')
plt.plot([datetime.datetime(2011,11,d) for d in range(20,27)],temp[min_temp_loc],'b-o',label='min')
plt.plot([datetime.datetime(2011,11,d) for d in range(20,27)],mean_temp,'g--o',label='mean')
plt.legend()
plt.xlim(datetime.datetime(2011,11,20),datetime.datetime(2011,11,26))
plt.grid()
plt.title('Maximum , Minimum and Mean Temperatue',fontsize=14,fontweight='bold')
plt.xlabel('Time',fontsize=12)
plt.ylabel('T[K]',fontsize=12)
plt.savefig('max_min_mean_temp.png',dpi=450)
plt.clf()

# Daily temperature 
plt.plot(np.arange(0,1440),smooth(daily_mean_temp,60))
plt.xticks(np.arange(0,1441,180),[f'{h//60:02d}'for h in np.arange(0,1441,180)])
plt.grid()
plt.title('Daily Temperature',fontweight='bold',fontsize=14)
plt.xlabel('Hour',fontsize=12)
plt.ylabel('T[K]',fontsize=12)
plt.savefig('daily_temp.png',dpi=450)
plt.clf()

# (saturated) water vapor pressure
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.plot(time,e,'b-',label='e')
plt.plot(time,es,'r-',label='es')
plt.grid()
plt.legend()
plt.title('Water Vapor Pressure and\nSaturated Water Vapor Pressure',fontweight='bold',fontsize=14)
plt.xlabel('Time',fontsize=12)
plt.ylabel('Pressure[hPa]',fontsize=12)
plt.savefig('e_es.png')
plt.clf()

#Daily e and es
plt.plot(np.arange(0,1440),smooth(daily_es_mean,60),label='es')
plt.plot(np.arange(0,1440),smooth(daily_e_mean,60),label='e')
plt.xticks(np.arange(0,1441,180),[f'{h//60:02d}'for h in np.arange(0,1441,180)])
plt.grid()
plt.title('Daily e and es',fontweight='bold',fontsize=14)
plt.xlabel('Hour',fontsize=12)
plt.ylabel('P[hPa]',fontsize=12)
plt.legend()
plt.savefig('daily_es.png',dpi=450)
plt.clf()


# RH time series
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.title('Relative Humidity',fontweight='bold',fontsize=14)
plt.xticks(rotation=45)
plt.plot(time,rh)
plt.grid()
plt.xlim(datetime.datetime(2011,11,19,23,59),datetime.datetime(2011,11,27,00,1))
plt.xlabel('Time',fontsize=12)
plt.ylabel('RH[%]',fontsize=12)
plt.savefig('rh.png',dpi=450)
plt.clf()

# daily relative humidity
plt.plot(np.arange(0,1440),smooth(daily_rh_mean,60))
plt.grid()
plt.xticks(np.arange(0,1441,120),[f'{h/60:02.0f}'for h in np.arange(0,1441,120)])
plt.xlim([0,1440])
plt.xlabel('Hour',fontsize=12)
plt.ylabel('RH [%]',fontsize=12)
plt.title('Daily RH',fontsize=12,fontweight='bold')
plt.savefig('rh_daily.png',dpi=450)
plt.clf()

# T-Td
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.plot(time,td-temp)
plt.xticks(rotation=45)
plt.title('Difference between Dew Point and Temperature',fontsize=14,fontweight='bold')
plt.grid()
plt.xlim(datetime.datetime(2011,11,19,23,59),datetime.datetime(2011,11,27,00,1))
plt.xlabel('Time',fontsize=12)
plt.ylabel('$T_d$-T [K]',fontsize=12)
plt.savefig('T_Td.png',dpi=450)
plt.clf()

# Specific Humidity
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.plot(time,qv)
plt.grid()
plt.title('Specific Humidity',fontweight='bold',fontsize=14)
plt.xlabel('Time',fontsize=12)
plt.ylabel('qv[kg/kg]',fontsize=12)
plt.savefig('qv.png',dpi=450)
plt.clf()

# wind rose
plt.figure()
ax=wr.WindroseAxes.from_ax()
ax.box(wd10,ws10,bins=np.arange(0,3.1,0.5),normed=True,cmap=cm.jet)
ax.set_legend(fontsize=12,bbox_to_anchor=[-0.1,-0.02],title='speed [m/s]')
ax.set_xticklabels([t.get_text() for t in ax.get_xticklabels()], fontsize=12)
ytick=np.arange(0,101,20)
ax.set_yticks(ytick)
ax.set_yticklabels([f'{y}%'for y in ytick],fontsize=12)
plt.title('Wind Rose 10-min Average 2011/11/20-26 @ NTUAS',y=1.05,fontsize=14,fontweight='bold')
plt.savefig('windrose.png',dpi=450)
plt.clf()

# wind speed time series
fig=plt.figure(figsize=(10,10))
plt.suptitle('Wind Speed',fontweight='bold',fontsize=16)
for i in range(7):
    ax=fig.add_subplot(3,3,i+1)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
    plt.title(datetime.date(2011,11,20+i),fontsize=14)
    plt.plot(time.iloc[1440*i:1440*(i+1)],ws[1440*i:1440*(i+1)])
    plt.plot(time.iloc[1440*i:1440*(i+1)],smooth(ws[1440*i:1440*(i+1)],60),'r')
    plt.xlabel('Hour',fontsize=12)
    plt.ylabel('ws [m/s]',fontsize=12)
    plt.ylim([0,8])
fig.legend(['ws','1hr-smooth'],bbox_to_anchor=(0.6,0.1),fontsize=14)
plt.tight_layout()
plt.savefig('day_ws.png',dpi=450)
plt.clf()


# wind direction time series
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.scatter(time,wd,s=[0.2])
plt.title('Weekly Wind Direction Scatter',fontweight='bold',fontsize=14)
plt.xlabel('Time',fontsize=12)
plt.ylabel('wd[o]',fontsize=12)
plt.xlim([datetime.datetime(2011,11,20),datetime.datetime(2011,11,27)])
plt.savefig('week_wd.png',dpi=450)
plt.clf()

fig=plt.figure(figsize=(10,10))
plt.suptitle('Wind Direction Scatter',fontweight='bold',fontsize=16)
for i in range(7):
    ax=fig.add_subplot(3,3,i+1)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
    plt.title(datetime.date(2011,11,20+i),fontsize=14)
    plt.scatter(time.iloc[1440*i:1440*(i+1)],wd[1440*i:1440*(i+1)],s=[0.3])
    plt.xlabel('Hour',fontsize=12)
    plt.ylabel('wd [deg]',fontsize=12)
    plt.ylim([0,360])
plt.tight_layout()
plt.savefig('day_wd.png',dpi=450)
plt.clf()

# Pressure
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.plot(time,pres)
plt.title('Pressure',fontweight='bold',fontsize=14)
plt.xlabel('Time',fontsize=12)
plt.ylabel('P [hPa]',fontsize=12)
plt.grid()
plt.savefig('p.png',dpi=450)