import numpy as np
import csv as csv
import matplotlib.pyplot as plt

def tloop(x,width):
    n=len(x)
    x=np.append(x,np.append(x,x))
    x_smooth=np.convolve(x,np.ones(width)/width,mode='same')
    xs=x_smooth[n:2*n]
    return xs

path='./cwa玉山氣象站467550-1943-2025-AirTemperature-month.csv'
file=open(path)
var=list(csv.reader(file,delimiter=','))
temp=[]
for i in range(1,len(var)-2+1):
    for j in range(1,13):
        if str(var[i][j])=='--' or str(var[i][j])=='X':
            temp.append(np.nan)
        else:
            temp.append(float(var[i][j]))

temp=np.array(temp).reshape((83,12))
nannum=np.isnan(temp).sum(axis=1)

avgTemp=np.mean(temp,axis=1)
avgTemp=np.where(nannum==0,avgTemp,np.nan)

Temptloop=tloop(avgTemp,10)

time=np.arange(1943,2026)


plt.plot(time,avgTemp,'b-')
plt.plot(time,Temptloop,'r-')
plt.title('Annually Average Temperature\n46755 Yushan Station',fontsize=14)
plt.xticks(np.arange(1940,2031,10),fontsize=10)
plt.yticks(np.arange(2,7.1,0.5),fontsize=10)
plt.xlim([1943,2025])
plt.ylim([2,7])
plt.xlabel('Year',fontsize=12)
plt.ylabel('$T_{avg}$ [$^{o}C$]',fontsize=12)
plt.legend(['Raw average','10-year Smoothing'],loc='upper left')
plt.grid()
plt.savefig('avgTemp_Yushan.png',dpi=500)

path='/home/B13/b13209015/mearsure/467480-2025-AirTemperature-month.csv'
file=open(path)
var=list(csv.reader(file,delimiter=','))
temp=[]
for i in range(1,len(var)-2+1):
    for j in range(1,13):
        if str(var[i][j])=='--' or str(var[i][j])=='X':
            temp.append(np.nan)
        else:
            temp.append(float(var[i][j]))

temp=np.array(temp).reshape((58,12))
nannum=np.isnan(temp).sum(axis=1)

avgTemp=np.mean(temp,axis=1)
avgTemp=np.where(nannum==0,avgTemp,np.nan)

Temptloop=tloop(avgTemp,10)

time=np.arange(1968,2026)

plt.clf()
plt.plot(time,avgTemp,'b-')
plt.plot(time,Temptloop,'r-')
plt.title('Annually Average Temperature\n46748 Chiayi Station',fontsize=14)
plt.xticks(np.arange(1960,2031,10),fontsize=10)
plt.yticks(np.arange(21,25.1,0.5),fontsize=10)
plt.xlim([1968,2025])
plt.ylim([21,25])
plt.xlabel('Year',fontsize=12)
plt.ylabel('$T_{avg}$ [$^{o}C$]',fontsize=12)
plt.legend(['Raw average','10-year Smoothing'],loc='upper left')
plt.grid()
plt.savefig('avgTemp_Chiayi.png',dpi=500)