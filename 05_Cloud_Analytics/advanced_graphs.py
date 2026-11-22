from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent

def main():
 d=pd.read_csv(ROOT/'server_logs.csv');req={'timestamp','path','status','response_ms'}
 if not req.issubset(d):raise ValueError('Missing log fields')
 d.timestamp=pd.to_datetime(d.timestamp,utc=True,errors='raise');d.status=pd.to_numeric(d.status,errors='raise');d.response_ms=pd.to_numeric(d.response_ms,errors='raise')
 if d[list(req)].isna().any().any() or not d.status.between(100,599).all() or (d.response_ms<0).any():raise ValueError('Invalid log data')
 out=ROOT/'graphs';out.mkdir(exist_ok=True)
 def save(fig,n):
  fig.tight_layout()
  for ext in ('png','svg'):fig.savefig(out/f'{n}.{ext}',dpi=300,bbox_inches='tight')
  plt.close(fig)
 s=d.status.value_counts().sort_index();fig,ax=plt.subplots();bars=ax.bar(s.index.astype(str),s.values,color=['#3b8b82' if v<400 else '#e5a346' if v<500 else '#bf5549' for v in s.index]);ax.bar_label(bars);ax.set(title='HTTP status distribution',xlabel='Status code',ylabel='Requests');ax.set_ylim(0,s.max()*1.2);save(fig,'fig_5_1_status')
 hours=d.set_index('timestamp').resample('1h').size();fig,ax=plt.subplots(figsize=(10,4));ax.plot(hours.index,hours.values,marker='o',color='#2a7694');ax.set(title=f'Hourly requests (peak: {hours.max()}, {sum(hours==hours.max())} tied hours)',xlabel='Hour (UTC)',ylabel='Requests');ax.set_ylim(0,hours.max()*1.2);ax.grid(alpha=.2);fig.autofmt_xdate();save(fig,'fig_5_2_hourly')
 p=d.path.value_counts().sort_values();fig,ax=plt.subplots();bars=ax.barh(p.index,p.values,color='#357e9e');ax.bar_label(bars);ax.set(title='Most accessed endpoints',xlabel='Requests');ax.set_xlim(0,p.max()*1.2);save(fig,'fig_5_3_endpoints')
 e=d[d.status>=400];fig,axes=plt.subplots(1,2,figsize=(10,4));series=e.set_index('timestamp').resample('1h').size().reindex(hours.index,fill_value=0);axes[0].plot(series.index,series.values,marker='o',color='#bc5446');axes[0].set(title='Errors per hour',ylabel='4xx and 5xx responses');fig.autofmt_xdate();c=e.status.value_counts().sort_index();bars=axes[1].bar(c.index.astype(str),c.values,color=['#e5a346','#bf5549']);axes[1].bar_label(bars);axes[1].set(title='Errors by status',xlabel='Status code',ylabel='Responses');axes[1].set_ylim(0,c.max()*1.2);save(fig,'fig_5_4_errors')
 result=ROOT/'outputs';result.mkdir(exist_ok=True);d.groupby('status').size().rename('requests').to_csv(result/'status_summary.csv');d.groupby('path').size().rename('requests').to_csv(result/'endpoint_summary.csv');print(f'{len(d)} requests; {len(e)} errors; {hours.max()} peak requests in {sum(hours==hours.max())} hours')
if __name__=='__main__':main()
