import pandas as pd
import pysolar
import datetime as datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

path='PSP_20081005.xls'
file=pd.read_excel(path)

lon=121.5390
lat=25.0148

time=list(file.iloc[:,0])
psp03=np.array(list(file.iloc[:,1]))
psp04=np.array(list(file.iloc[:,2]))
psp07=np.array(list(file.iloc[:,3]))
ang=[]
Z=[]

for t in time:
    date=datetime.datetime(t.year,t.month,t.day,t.hour,t.minute,tzinfo=datetime.timezone(datetime.timedelta(hours=8)))
    zang=pysolar.solar.get_altitude(lat,lon,date)
    ang.append(zang)
    Z.append(pysolar.radiation.get_radiation_direct(date,zang))
ang=np.array(ang)
ang=90-ang

plt.clf()
plt.gca().xaxis.set_major_formatter(mdate.DateFormatter('%H'))
plt.gca().xaxis.set_major_locator(mdate.HourLocator(interval=1))
plt.title('2008/10/5 Solar Irradiance',fontsize=14)
plt.plot(time,Z,'k--')
plt.plot(time,psp03,'r-')
plt.plot(time,psp04,'b-')
plt.plot(time,psp07,'g-')
plt.yticks(np.arange(0,1001,100),fontsize=10)
plt.xlim([time[190],time[1151]])
plt.ylim([0,1000])
plt.grid()
plt.xlabel('Time [Hour]',fontsize=12)
plt.ylabel('Irradiance [$W/m^2$]',fontsize=12)
plt.legend(['Z (TSI)','A (0.3~3 $\mu$m)','B (0.4~3 $\mu$m)','C (0.7~3 $\mu$m)'],bbox_to_anchor=(0.8, 1), loc="upper left")
plt.tight_layout()
plt.savefig('z.png',dpi=500)

plt.clf()
fig,ax=plt.subplots(2,2)

ax[0,0].xaxis.set_major_formatter(mdate.DateFormatter('%H'))
ax[0,0].xaxis.set_major_locator(mdate.HourLocator(interval=2))
ax[0,0].set_title('(A-B)/A')
ax[0,0].plot(time,(psp03-psp04)/psp03,'b')
ax[0,0].set_xlim([time[190],time[1151]])
ax[0,0].set_xlabel('Time [Hour]')
ax[0,0].set_yticks(np.arange(0,0.31,0.05))
ax[0,0].grid()


ax[0,1].xaxis.set_major_formatter(mdate.DateFormatter('%H'))
ax[0,1].xaxis.set_major_locator(mdate.HourLocator(interval=2))
ax[0,1].set_title('(B-C)/A')
ax[0,1].plot(time,(psp04-psp07)/psp03,'b')
ax[0,1].set_xlim([time[190],time[1151]])
ax[0,1].set_xlabel('Time [Hour]')
ax[0,1].set_yticks(np.arange(0.4,0.91,0.1))
ax[0,1].grid()


ax[1,0].xaxis.set_major_formatter(mdate.DateFormatter('%H'))
ax[1,0].xaxis.set_major_locator(mdate.HourLocator(interval=2))
ax[1,0].set_title('C/B')
ax[1,0].plot(time,psp07/psp04,'b')
ax[1,0].set_xlim([time[190],time[1151]])
ax[1,0].set_xlabel('Time [Hour]')
ax[1,0].set_yticks(np.arange(0,0.51,0.1))
ax[1,0].grid()


ax[1,1].xaxis.set_major_formatter(mdate.DateFormatter('%H'))
ax[1,1].xaxis.set_major_locator(mdate.HourLocator(interval=2))
ax[1,1].set_title('A/Z')
ax[1,1].plot(time,psp03/Z,'b')
ax[1,1].set_xlim([time[190],time[1151]])
ax[1,1].set_xlabel('Time [Hour]')
ax[1,1].set_yticks(np.arange(0,3.1,0.5))
ax[1,1].grid()

plt.tight_layout()
plt.savefig('ratio.png',dpi=500)