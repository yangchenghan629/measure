import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt , matplotlib.cm as cm , matplotlib.colors as mcolors
import PIL as pil
from mpl_toolkits.basemap import Basemap

colorlevel = [0,1,2,6,10,15,20,30,40,50,70,90,110,130,150,200,300,400]
precip_data=['None','#9BFFFF','#00CFFF','#0198FF','#0165FF','#309901',\
          '#32FF00','#F8FF00','#FFCB00','#FF9A00','#FA0300','#CC0003',\
          '#A00000','#98009A','#C304CC','#F805F3','#FECBFF']
cmaps = mcolors.ListedColormap(precip_data,'precipitation')
norms = mcolors.BoundaryNorm(colorlevel, cmaps.N)

lon=nc.Dataset('GPM_202106/3B-DAY.MS.MRG.3IMERG.20210601-S000000-E235959.V06.nc4.SUB.nc4').variables['lon'][:]
lat=nc.Dataset('GPM_202106/3B-DAY.MS.MRG.3IMERG.20210601-S000000-E235959.V06.nc4.SUB.nc4').variables['lat'][:]
prec=np.full((30,420,320),np.nan)
for i in range(1,31):
    prec[i-1,:,:]=nc.Dataset(f'GPM_202106/3B-DAY.MS.MRG.3IMERG.202106{i:02d}-S000000-E235959.V06.nc4.SUB.nc4').variables['precipitationCal'][:,:,:]

lon2,lat2=np.meshgrid(lon,lat)
for i in range(1,31):
    plt.clf()
    m=Basemap(projection='cyl',llcrnrlon=lon[0],urcrnrlon=lon[-1],llcrnrlat=lat[0],urcrnrlat=lat[-1])
    m.drawcoastlines()
    cx,cy=m(lon2,lat2)
    cs=m.contourf(cx,cy,prec[i-1,:,:].T,cmap=cmaps,norm=norms,levels=colorlevel,extend='max')
    plt.colorbar(cs,label='Precipitation (mm)',ticks=colorlevel)
    plt.xticks(np.arange(100,141,10),fontsize=10)
    plt.yticks(np.arange(10,41,5),fontsize=10)
    plt.xlabel('Lon',fontsize=12)
    plt.ylabel('Lat',fontsize=12)
    plt.title(f'Precipitation on {i:02d} June 2021',fontsize=14)
    plt.tight_layout()
    plt.savefig(f'./daily_prec/daily_prec.{i:02d}.png',dpi=450)
    plt.close()

gif=[]
for i in range(1,31):
    gif.append(pil.Image.open(f'./daily_prec/daily_prec.{i:02d}.png'))
gif[0].save('daily_prec.gif',save_all=True,append_images=gif[1:],duration=500,loop=0)

m=Basemap(projection='cyl',llcrnrlat=lat[0],urcrnrlat=lat[-1],llcrnrlon=lon[0],urcrnrlon=lon[-1])
m.drawcoastlines()
cx,cy=m(lon2,lat2)
cs=m.contourf(cx,cy,np.mean(prec,axis=0).T,cmap=cm.jet,levels=np.arange(0,50,5),extend='max')
plt.colorbar(cs,label='Precipitation (mm)')
plt.xticks(np.arange(100,141,10),fontsize=10)
plt.yticks(np.arange(10,41,5),fontsize=10)
plt.xlabel('Lon',fontsize=12)
plt.ylabel('Lat',fontsize=12)
plt.title('Mean Precipitation in June 2021',fontsize=14)
plt.tight_layout()
plt.savefig('mean_prec.png',dpi=450)
plt.close()