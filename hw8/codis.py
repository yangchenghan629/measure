import pandas as pd
import numpy as np
import matplotlib.pyplot as plt ,matplotlib.dates as mdates
import datetime

station=[('466920','Taipei'),('467490','Taichung'),('467410','Tainan'),('466990','Hualien')]
for s in station:
    codis=pd.read_csv(f'{s[0]}-2021-06.csv')
    pres=codis.iloc[1:,2].to_numpy(dtype='float')
    temp=codis.iloc[1:,7].to_numpy(dtype='float')
    precp=codis.iloc[1:,21].to_numpy()
    precp=np.array(np.where(precp!='T',precp,0),dtype='float')
    ws=codis.iloc[1:,16].to_numpy(dtype='float')
    wd=codis.iloc[1:,17].to_numpy(dtype='float')

    date=[datetime.datetime(2021,6,d)for d in range(1,31)]

    fig,ax=plt.subplots(layout='constrained')
    ax2=ax.twinx()
    ax3=ax.twinx()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    ax.plot(date,pres,'r-',label='Pres')
    ax.tick_params(axis='x',rotation=45)
    ax.set_xlim(date[0],date[-1])
    ax.set_ylim(1000,1015)
    ax.set_xlabel('Date')
    ax.set_ylabel('Pressure [hPa]')
    ax2.plot(date,temp,'k-',label='Temp')
    ax2.set_ylim(22,34)
    ax2.set_ylabel('Temperature [degC]')
    ax3.bar(date,precp,color='b',alpha=0.5,label='Prec')
    ax3.spines['right'].set_position(('axes',1.15))
    ax3.set_ylim(0,200)
    ax3.set_ylabel('Precipitation [mm]')
    fig.suptitle(f'June 2021 @ {s[1]} Station',fontsize=14)
    ax.grid(axis='both',which='major')
    ax2.grid(False)
    ax3.grid(False)
    fig.legend(ncols=3,bbox_to_anchor=(0.5,-0.05),loc='center')
    plt.savefig(f'{s[1]}.png',dpi=500,bbox_inches='tight')

