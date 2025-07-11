import pandas as pd
import numpy as np
import matplotlib.pyplot as plt , matplotlib.dates as mdates , matplotlib.colors as mcolors , matplotlib.cm as cm
import datetime as datetime
from tools import Thermo

# read data
# cl31
cldbase=pd.read_csv('20240731_CLdbase_alter.csv')
time=cldbase.iloc[:,0]
status=cldbase.iloc[:,1].to_numpy()
height1=cldbase.iloc[:,2].to_numpy()
mask1=(status==1)
height1=np.where(mask1,height1,np.nan)
mask2=(status==2)
height2=np.where(mask2,cldbase.iloc[:,3].to_numpy(),np.nan)
mask3=(status==3)
height3=np.where(mask3,cldbase.iloc[:,4].to_numpy(),np.nan)


time=[]
for h in range(0,24):
    for m in range(0,60):
        for s in range(0,60,5):
            time.append(datetime.datetime(2024,7,31,h,m,s))

levels=np.arange(5,7501,5)
backsca=pd.read_csv('20240731_backsca_alter.csv').iloc[:,1:].to_numpy()
backsca=np.where(backsca>=0,backsca,0)

# surface data
sfc=pd.read_csv('NTU_stn_20240731.csv')
pres=sfc.iloc[:,1].to_numpy()
temp=sfc.iloc[:,2].to_numpy()
Td=sfc.iloc[:,3].to_numpy()
rh=sfc.iloc[:,4].to_numpy()
es=Thermo.cc_equation(temp+273.15)
e=es*rh/100
qv=Thermo.epsilon*e/(pres-e)
Tc=[]
Zc=[]
for i in range(len(temp)):
    h=0
    parcel_temp=temp[i]+273.15 # K
    es_parcel=Thermo.cc_equation(parcel_temp) #hPa
    Tv=parcel_temp*(1+0.608*qv[i]) #K
    p=pres[i] #hPa
    qvs=Thermo.epsilon*es_parcel/(p-es_parcel) # kg/kg
    while(qv[i]<=qvs):
        h+=5
        parcel_temp-=5*0.0098
        p/=np.exp(9.8*5/(287*Tv))
        es_parcel=Thermo.cc_equation(parcel_temp)
        qvs=Thermo.epsilon*es_parcel/(p-es_parcel)
        if h>7500 or qvs<0:
            qvs=np.nan
            h=np.nan
            break
    Tc.append(parcel_temp)
    Zc.append(h)

fig,ax=plt.subplots()
fig.suptitle('Temperature and Relative Humidity',fontsize=14)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax2=ax.twinx()
ax.plot(time[::12],temp,'b-',label='temp')
ax2.plot(time[::12],rh,'r--',label='RH')
fig.legend()
ax.set_ylim(24,38)
ax2.set_ylim(50,100)
ax.grid(True)
ax2.grid(False)
ax.set_ylabel('T (degC)')
ax.set_xlabel('Time (hr)')
ax2.set_ylabel('RH (%)')
plt.savefig('temp_rh.png',dpi=450)

# plt.figure(figsize=(6,4))
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H'))
# plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
# plt.scatter(time,height1,s=[1.2],c=['blue'])
# plt.scatter(time,height2,s=[1.2],c=['orange'])
# plt.scatter(time,height3,s=[1.2],c=['red'])
# plt.xlim(datetime.datetime(2024,7,31,0,0,0),datetime.datetime(2024,8,1,0,0,0))
# plt.ylim([0,5000])
# plt.xlabel('Time (hr)',fontsize=12)
# plt.ylabel('Cloud Base Height (m)',fontsize=12)
# plt.title('Cloud Base Height on 31 July 2024',fontsize=14)
# plt.grid()
# plt.savefig('cloudbase.png',dpi=450)

# plt.clf()
# time2,lev2=np.meshgrid(time,levels)
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H'))
# plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
# plt.pcolormesh(time2,lev2,backsca.T,cmap=cm.jet,vmin=0,vmax=3e+4)
# plt.colorbar(label='Backsca Coef ($10^{-6}srad^{-1}km^{-1}$)',format='%.1e')
# plt.xlabel('Time (hr)')
# plt.ylabel('Height (m)')
# plt.title('Backscatter Coefficient on 31 July 2024',fontsize=14)
# plt.savefig('backsca.png',dpi=450)

# plt.clf()
# time2,lev2=np.meshgrid(time,levels)
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H'))
# plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
# plt.pcolormesh(time2,lev2,backsca.T,cmap=cm.jet,vmin=0,vmax=3e+4)
# plt.colorbar(label='Backsca Coef ($10^{-6}srad^{-1}km^{-1}$)',format='%.1e')
# plt.plot(time,height1,'k',linewidth=0.5)
# plt.xlabel('Time (hr)')
# plt.ylabel('Height (m)')
# plt.title('Backscatter Coefficient and Cloud Base on 31 July 2024',fontsize=14)
# plt.savefig('backsca_cbh.png',dpi=450)


# plt.clf()
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H'))
# plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
# plt.plot(time,height1,'b-',label='CL31')
# plt.plot(time[::12],Zc,'r-',label='Parcel Lifting')
# plt.xlabel('Time (hr)',fontsize=12)
# plt.ylabel('Height (m)',fontsize=12)
# plt.title('Cloud Base Height on 31 July 2024',fontsize=14)
# plt.legend()
# plt.grid()
# plt.savefig('cl31_parcel.png',dpi=450)
# plt.clf()
