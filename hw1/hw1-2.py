import csv as csv
import matplotlib.pyplot as plt
import numpy as np


def tloop(x,width):
    n=len(x)
    x=np.append(x,np.append(x,x))
    x_smooth=np.convolve(x,np.ones(width)/width,mode='same')
    xs=x_smooth[n:2*n]
    return xs

path='cwa玉山氣象站467550-1943-2025-AirTemperature-month.csv'
file=open(path)
var=list(csv.reader(file))
temp=[]
for i in range(1,len(var)-1):
    for j in range(1,13):
        if var[i][j]=='--' or var[i][j]=='X':
            temp.append(np.nan)
        else:
            temp.append(float(var[i][j]))
temp=np.array(temp).reshape((len(var)-2,12))

winter=np.zeros(len(var)-2)
winter[:]=np.nan
for i in range(1,len(var)-3):
    winter[i]=(temp[i-1][10]+temp[i-1][11]+temp[i][0]+temp[i][1])/4

wintertloop=tloop(winter,10)

time=np.arange(1943,2026)
plt.title('Annually Winter Average Temperature\n46755 Yushan Station',fontsize=14)
plt.plot(time,winter,'b')
plt.plot(time,wintertloop,'r-')
plt.legend(['Raw Average','10-year Smoothing'])
plt.xticks(np.arange(1940,2026,10),fontsize=10)
plt.yticks(np.arange(-3,5.1,1),fontsize=10)
plt.xlim([1943,2025])
plt.ylim([-3,5])
plt.xlabel('Year',fontsize=12)
plt.ylabel('$T_{avg}$ [$^oC$]',fontsize=12)
plt.grid()
plt.savefig('winter.png',dpi=500)