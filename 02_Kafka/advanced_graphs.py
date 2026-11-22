from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent

def main():
    d=pd.read_csv(ROOT/'outputs/traffic_events.csv'); req={'timestamp','sensor_id','speed_kmh','vehicles','congestion_alert'}
    if not req.issubset(d):raise ValueError('Missing traffic fields')
    d.timestamp=pd.to_datetime(d.timestamp,utc=True,errors='raise');d['alert']=d.congestion_alert.astype(str).str.lower().map({'true':True,'false':False})
    if d[list(req)].isna().any().any() or d.alert.isna().any() or not (d.alert==((d.speed_kmh<25)&(d.vehicles>=30))).all():raise ValueError('Invalid events or alerts')
    out=ROOT/'graphs';out.mkdir(exist_ok=True)
    def save(fig,n):
        fig.tight_layout()
        for ext in ('png','svg'):fig.savefig(out/f'{n}.{ext}',dpi=300,bbox_inches='tight')
        plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,5));
    for sensor,g in d.groupby('sensor_id'):ax.plot(g.timestamp,g.speed_kmh,marker='.',label=sensor,alpha=.8)
    a=d[d.alert];ax.scatter(a.timestamp,a.speed_kmh,marker='x',s=70,color='red',label='Alert',zorder=4);ax.axhline(25,color='black',linestyle='--',label='Speed threshold (<25 km/h)');ax.set(title='Recorded sensor speeds and alerts',xlabel='Event time (UTC)',ylabel='Speed (km/h)');ax.legend(ncol=2,fontsize=8);fig.autofmt_xdate();save(fig,'fig_2_1_sensor_time')
    s=d.groupby('sensor_id').alert.sum();fig,ax=plt.subplots(figsize=(8,4));bars=ax.bar(s.index,s.values,color='#c76d34');ax.bar_label(bars);ax.set(title='Congestion alerts by sensor',xlabel='Sensor',ylabel='Alert events');ax.set_ylim(0,max(1,s.max())*1.3);save(fig,'fig_2_2_alerts_by_sensor')
    g=d.groupby('sensor_id').agg(volume=('vehicles','sum'),speed=('speed_kmh','mean'),events=('alert','size'),alerts=('alert','sum'));fig,axes=plt.subplots(1,2,figsize=(10,4));
    for ax,col,title in zip(axes,['volume','speed'],['Sum of observed vehicle counts','Mean speed (km/h)']):
        bars=ax.bar(g.index,g[col],color='#36799a');ax.bar_label(bars,fmt='%.1f' if col=='speed' else '%.0f',padding=3);ax.set(title=title,xlabel='Sensor');ax.set_ylim(0,g[col].max()*1.2)
    save(fig,'fig_2_3_volume_speed')
    fig,ax=plt.subplots(figsize=(7,4));counts=d.alert.value_counts().reindex([False,True],fill_value=0);bars=ax.bar(['No alert','Alert'],counts.values,color=['#3985a5','#d47836']);ax.bar_label(bars);ax.set(title='Event alert classification',ylabel='Events');ax.set_ylim(0,counts.max()*1.2);save(fig,'fig_2_4_event_status');g.to_csv(ROOT/'outputs/sensor_summary.csv');print(g.to_string())
if __name__=='__main__':main()
