from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent

def main():
    d=pd.read_csv(ROOT/'server_logs.csv',parse_dates=['timestamp'])
    required={'timestamp','status','path'}
    if not required.issubset(d): raise ValueError(f'Missing columns: {required-set(d.columns)}')
    d['status']=pd.to_numeric(d.status,errors='raise')
    if d[list(required)].isna().any().any() or not d.status.between(100,599).all(): raise ValueError('Invalid log rows')
    d['hour']=d.timestamp.dt.hour
    charts=[('01_http_status_distribution','HTTP response statuses','Status','Requests',d.status.value_counts().sort_index()),('02_requests_per_hour','Requests by UTC hour','Hour (UTC)','Requests',d.hour.value_counts().reindex(range(24),fill_value=0)),('03_most_accessed_endpoints','Requests by endpoint','Endpoint','Requests',d.path.value_counts()),('04_error_trends','HTTP errors by UTC hour','Hour (UTC)','Errors',d[d.status>=400].hour.value_counts().reindex(range(24),fill_value=0))]
    out=ROOT/'graphs';out.mkdir(exist_ok=True)
    for name,title,x,y,s in charts:
        fig,ax=plt.subplots(figsize=(11,5)); b=ax.bar([str(v) for v in s.index],s.values,color='#286491');ax.bar_label(b,fontsize=8,padding=2);ax.set(title=title,xlabel=x,ylabel=y);ax.set_ylim(0,max(1,s.max())*1.2);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True);fig.tight_layout()
        for ext in ('png','svg'):fig.savefig(out/f'{name}.{ext}',dpi=300,bbox_inches='tight')
        plt.close(fig)
    print(f'{len(d)} requests; {(d.status>=400).sum()} errors; generated charts in {out}')
if __name__=='__main__': main()
