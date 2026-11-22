from pathlib import Path
import re
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent

def main():
    path=ROOT/'outputs/flink_run.log'
    if not path.exists(): raise SystemExit(f'No Flink execution log: {path}; run the job and save taskmanager logs first.')
    text=path.read_text(encoding='utf-8');pat=r'READING (P\d+) ts=(\d+) heart=(\d+) temperature=([\d.]+)';rows=re.findall(pat,text)
    sums=re.findall(r'SUMMARY patient=(P\d+) window=\[(\d+),(\d+)\) count=(\d+) mean_heart=([\d.]+) mean_temp=([\d.]+)',text)
    if not rows or not sums:raise SystemExit('Flink log has no READING or SUMMARY records; rerun the current job and capture its taskmanager logs.')
    d=pd.DataFrame(rows,columns=['patient','timestamp','heart','temp']);
    for c in ['timestamp','heart','temp']:d[c]=pd.to_numeric(d[c],errors='raise')
    d['time']=pd.to_datetime(d.timestamp,unit='ms',utc=True);d['alert']=(d.heart>120)|(d.temp>=38)
    w=pd.DataFrame(sums,columns=['patient','start','end','count','mean_heart','mean_temp']);
    for c in ['start','end','count','mean_heart','mean_temp']:w[c]=pd.to_numeric(w[c],errors='raise')
    if len(d)!=60 or len(w)!=18 or int(w['count'].sum())!=len(d):raise ValueError('Unexpected or duplicate runtime output; capture only one complete job run')
    alerts=re.findall(r'ALERT (P\d+) ts=(\d+) heart=(\d+) temperature=([\d.]+)',text)
    expected={(r.patient,str(r.timestamp),str(r.heart),str(r.temp)) for r in d[d.alert].itertuples()}
    if set(alerts)!=expected or len(alerts)!=len(expected): raise ValueError('Alert output does not reconcile with readings')
    for row in w.itertuples():
        subset=d[(d.patient==row.patient)&(d.timestamp>=row.start)&(d.timestamp<row.end)]
        if row.end-row.start!=10000 or len(subset)!=row.count or abs(subset.heart.mean()-row.mean_heart)>0.051 or abs(subset.temp.mean()-row.mean_temp)>0.051: raise ValueError('Window output does not reconcile with readings')
    out=ROOT/'graphs';out.mkdir(exist_ok=True)
    def save(fig,n):
        fig.tight_layout()
        for ext in ('png','svg'):fig.savefig(out/f'{n}.{ext}',dpi=300,bbox_inches='tight')
        plt.close(fig)
    fig,axes=plt.subplots(2,1,figsize=(10,7),sharex=True)
    for patient,g in d.groupby('patient'):
        axes[0].plot(g.time,g.heart,marker='.',label=patient);axes[1].plot(g.time,g.temp,marker='.',label=patient)
    for ax,v,label in [(axes[0],120,'Heart rate (bpm)'),(axes[1],38,'Temperature (°C)')]:ax.axhline(v,color='red',linestyle='--',label='Demo threshold');ax.set_ylabel(label);ax.legend(ncol=4,fontsize=8)
    axes[0].set_title('Synthetic patient vital signs');axes[1].set_xlabel('Event time (UTC)');fig.autofmt_xdate();save(fig,'01_vital_signs_over_time')
    counts=d.groupby('patient').alert.sum();fig,ax=plt.subplots();bars=ax.bar(counts.index,counts.values,color='#c57237');ax.bar_label(bars);ax.set(title='Threshold alerts by patient',ylabel='Alert readings',xlabel='Patient');ax.set_ylim(0,max(counts)*1.2+1);save(fig,'02_threshold_alerts')
    w['time']=pd.to_datetime(w.start,unit='ms',utc=True);fig,ax=plt.subplots(figsize=(9,5));
    for p,g in w.groupby('patient'):ax.plot(g.time,g.mean_heart,marker='o',label=p)
    ax.set(title='Mean heart rate by 10-second event-time window',xlabel='Window start (UTC)',ylabel='Mean heart rate (bpm)');ax.legend();fig.autofmt_xdate();save(fig,'03_window_aggregations')
    fig,ax=plt.subplots();counts=d.alert.value_counts().reindex([False,True],fill_value=0);bars=ax.bar(['Normal','Alert'],counts.values,color=['#3886a4','#ca7138']);ax.bar_label(bars);ax.set(title='Reading classification',ylabel='Readings');ax.set_ylim(0,max(counts)*1.2);save(fig,'04_reading_classification');d.to_csv(ROOT/'outputs/readings.csv',index=False);w.to_csv(ROOT/'outputs/window_summary.csv',index=False);print(f'Flink processed {len(d)} readings, {d.alert.sum()} flagged, {len(w)} windows')
if __name__=='__main__':main()
