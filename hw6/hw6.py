import numpy as np
import datetime as dt
import matplotlib.pyplot as plt , matplotlib.lines as mlines , matplotlib.dates as mdates
import pandas as pd
from tools import Wind as wind

######################
# READ　DATA
######################
# RS41 
height=np.loadtxt('edt2_20231113_0555.txt',usecols=2,skiprows=6)
ascrate=np.loadtxt('edt2_20231113_0555.txt',usecols=1,skiprows=6)
temp=np.loadtxt('edt2_20231113_0555.txt',usecols=4,skiprows=6)
RH=np.loadtxt('edt2_20231113_0555.txt',usecols=5,skiprows=6)
pres=np.loadtxt('edt2_20231113_0555.txt',usecols=3,skiprows=6)
wd=np.loadtxt('edt2_20231113_0555.txt',usecols=7,skiprows=6)
ws=np.loadtxt('edt2_20231113_0555.txt',usecols=8,skiprows=6)

# LORA
lora=pd.read_csv('/home/B13/b13209015/measure/hw6/LoRa_20231113_062740.csv')

lora_time=[dt.datetime.fromisoformat(t.replace("Z", "+00:00")) for t in lora.iloc[:,0]]

lora_temp=lora.iloc[:,3].to_numpy()/100 # deg C
lora_RH=lora.iloc[:,4].to_numpy()/10 # %
lora_pres=lora.iloc[:,5].to_numpy()/100 # hPa
lora_height=lora.iloc[:,9].to_numpy()/100 # m
lora_ws=(lora.iloc[:,14].to_numpy()/100)*1000/3600 # m/s
lora_wd=(lora.iloc[:,16].to_numpy()/1000)%360 # deg

############################
# CALCULATION
############################
u,v=wind.wswd_to_uv(ws,wd)
lora_u,lora_v=wind.wswd_to_uv(lora_ws,lora_wd)

#############################
# GRAPHING
#############################
#RS41
fig,ax=plt.subplots(2,3,sharey='row')
ax[0,0].plot(temp,height,'#1f77b4')
ax[0,0].set_title('Temperature',fontsize=12)
ax[0,0].set_xlabel('T [K]',fontsize=10)
ax[0,0].set_ylabel('Height [m]',fontsize=10)
ax[0,0].set_xticks(np.arange(-40,21,15))
ax[0,0].set_xlim([-40,20])
ax[0,0].set_ylim([0,10000])
ax[0,0].grid()

ax[0,1].plot(RH,height,'#1f77b4')
ax[0,1].set_title('RH',fontsize=12)
ax[0,1].set_xlabel('RH [%]',fontsize=10)
ax[0,1].set_xticks(np.arange(0,101,20))
ax[0,1].set_xlim([0,100])
ax[0,1].set_ylim([0,10000])
ax[0,1].grid()

ax[0,2].plot(pres,height,'#1f77b4')
ax[0,2].set_title('Pressure',fontsize=12)
ax[0,2].set_xlabel('P [hPa]',fontsize=10)
ax[0,2].set_xticks(np.arange(1050,200,-200))
ax[0,2].set_ylim([0,10000])
ax[0,2].grid()

ax[1,0].plot(ws,height,'#1f77b4')

ax[1,0].set_title('Wind Speed',fontsize=12)
ax[1,0].set_xlabel('speed [m/s]',fontsize=10)
ax[1,0].set_ylabel('Height [m]',fontsize=10)
ax[1,0].set_xticks(np.arange(0,201,10))
ax[1,0].set_xlim([0,40])
ax[1,0].set_ylim([0,10000])
ax[1,0].grid()

ax[1,1].barbs(np.full(len(ws),30)[::100],height[::100],u[::100],v[::100],sizes=dict(emptybarb=0),barb_increments=dict(half=5,full=10,flag=50),length=6,color='#1f77b4')
ax[1,1].set_title('Wind Barb',fontsize=12)
ax[1,1].set_xticks([30,60],['RS41','ST'],rotation=45)
ax[1,1].set_xlim([0,90])
ax[1,1].set_ylim([0,10000])
ax[1,1].grid()

# LORA
ax[0,0].plot(lora_temp,lora_height,'r')
ax[0,1].plot(lora_RH,lora_height,'r')
ax[0,2].plot(lora_pres,lora_height,'r')
ax[1,0].plot(lora_ws,lora_height,'r')
ax[1,1].barbs(np.full(len(lora_ws),60)[::30],lora_height[::30],lora_u[::30],lora_v[::30],sizes=dict(emptybarb=0),barb_increments=dict(half=5,full=10,flag=50),length=6,color='r')

fig.delaxes(ax[1,2])

legend_element=[mlines.Line2D([0],[0],color='#1f77b4',linewidth=2,label='RS41'),mlines.Line2D([0],[0],color='r',label='Storm Tracker')]
fig.legend(handles=legend_element,ncols=1,bbox_to_anchor=(0.95,0.2))
plt.suptitle('RS41 and Storm-Tracker Radiosonde Data',fontsize=14)

plt.tight_layout()
plt.savefig('hw6_1.png',dpi=500)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=1))
plt.plot(lora_time,lora_height,'.-')
plt.xticks(rotation=45)
plt.xlim([lora_time[0],lora_time[-1]])
plt.ylim([0,np.max(lora_height)+100])


plt.plot(lora_ws,lora_height,'.-')
plt.ylim([0,np.max(lora_height)+100])
