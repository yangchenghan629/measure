import numpy as np
import matplotlib.pyplot as plt

w=150/60 # m/sec
def cot(t):
    return 1/np.tan(t)

data=[]
with open('TD105 data sample.txt') as f:
    lines=f.readlines()
    for line in lines:
        if '*' in line:
            line=line.replace('*',' ')
        if '\n'!=line:
            line=line.replace('\n','')
            data.append(line.split(' '))
data=np.array(data[1:-1])

A=np.radians(data[:,2].astype('float'))
E=np.radians(data[:,3].astype('float'))

u=np.full((len(A)),np.nan)
v=np.full((len(A)),np.nan)
time=np.arange(0,1041,10) #sec

for i in range(len(A)-1):
    u[i]=w*time[i+1]*cot(E[i+1])*np.sin(A[i+1])-w*time[i]*cot(E[i])*np.sin(A[i])
    v[i]=w*time[i+1]*cot(E[i+1])*np.cos(A[i+1])-w*time[i]*cot(E[i])*np.cos(A[i])
u/=10
v/=10


u=np.where(np.abs(u)<100,u,np.nan)
v=np.where(np.abs(v)<100,v,np.nan)

ws=(u**2+v**2)**0.5
wd=(np.degrees(np.arctan2(-u,-v))+360)%360

plt.plot(ws,time*w)
plt.grid()
plt.ylim([0,3000])
plt.xlabel('wind speed [m/s]',fontsize=12)
plt.ylabel('Height [m]',fontsize=12)
plt.title('Wind Speed',fontweight='bold',fontsize=14)
plt.savefig('ws.png',dpi=500)
plt.clf()

step=2
plt.figure(figsize=(6,5))
plt.barbs(np.zeros(len(time))[::step],time[::step]*w,u[::step],v[::step],length=6,barb_increments=dict(half=1,full=5,flag=10),sizes=dict(emptybarb=0))
plt.xticks([])
plt.ylabel('Height [m]',fontsize=12)
plt.title('Wind Barb',fontweight='bold',fontsize=14)
plt.savefig('barb.png',dpi=500)
plt.clf()

plt.plot(ws,time*w)
plt.barbs(np.full((len(time)),4)[::step],time[::step]*w,u[::step],v[::step],length=6,barb_increments=dict(half=1,full=5,flag=10),sizes=dict(emptybarb=0))
plt.yticks(np.arange(0,2601,200))
plt.xlim([0,8])
plt.ylim([0,2600])
plt.grid()
plt.title('Wind Speed and Direction',fontweight='bold',fontsize=14)
plt.xlabel('Speed [m/s]',fontsize=12)
plt.ylabel('Height [m]',fontsize=12)
plt.savefig('wind.png',dpi=500)
