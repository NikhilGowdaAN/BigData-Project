from pathlib import Path
import argparse
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--input',type=Path,default=ROOT/'outputs'/'traffic_events.csv'); args=parser.parse_args()
    if not args.input.exists(): raise SystemExit(f'No consumed event file: {args.input}. Run the consumer with --output first.')
    d=pd.read_csv(args.input); cols={'sensor_id','timestamp','speed_kmh','vehicles','congestion_alert'}
    if not cols.issubset(d.columns): raise SystemExit(f'Missing columns: {cols-set(d.columns)}')
    try:
        d['timestamp']=pd.to_datetime(d.timestamp,utc=True,errors='raise')
        for c in ('speed_kmh','vehicles'): d[c]=pd.to_numeric(d[c],errors='raise')
        alerts=d.congestion_alert.astype(str).str.lower()
        if not alerts.isin(['true','false']).all(): raise ValueError('Invalid alert values')
        d['alert']=alerts.eq('true')
        if d.empty or d[list(cols)].isna().any().any() or (d[['speed_kmh','vehicles']]<0).any().any(): raise ValueError('Empty or invalid measurements')
        if not (d.alert == ((d.speed_kmh<25)&(d.vehicles>=30))).all(): raise ValueError('Alerts do not match the demonstration rule')
    except ValueError as e: raise SystemExit(f'Invalid traffic data: {e}')
    series=[('01_traffic_volume_by_road','Observed traffic volume by sensor','Sensor','Vehicles (sum)',d.groupby('sensor_id').vehicles.sum()),('02_average_speed_by_road','Average speed by sensor','Sensor','Speed (km/h)',d.groupby('sensor_id').speed_kmh.mean()),('03_congestion_alerts_over_time','Congestion alerts per minute (UTC)','Minute (UTC)','Alerts',d.set_index('timestamp').alert.resample('1min').sum()),('04_traffic_event_distribution','Traffic event status','Status','Events',d.alert.map({True:'Congestion alert',False:'No alert'}).value_counts().reindex(['Congestion alert','No alert'],fill_value=0))]
    out=ROOT/'graphs';out.mkdir(exist_ok=True)
    for name,title,x,y,s in series:
        labels=[v.strftime('%H:%M') if isinstance(v,pd.Timestamp) else str(v) for v in s.index]
        fig,ax=plt.subplots(figsize=(10,5)); bars=ax.bar(labels,s.values,color='#286491');ax.bar_label(bars,fmt='%.1f' if 'speed' in name else '%.0f',padding=3);ax.set(title=title,xlabel=x,ylabel=y);ax.set_ylim(0,max(1,s.max())*1.2);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True);fig.autofmt_xdate(rotation=30);fig.tight_layout()
        for ext in ('png','svg'):fig.savefig(out/f'{name}.{ext}',dpi=300,bbox_inches='tight')
        plt.close(fig)
    print(f'Graphed {len(d)} Kafka-consumed events; {d.alert.sum()} congestion alerts; output: {out}')
if __name__=='__main__':main()
