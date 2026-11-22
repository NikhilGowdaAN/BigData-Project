import csv, json, argparse
from collections import Counter
from pathlib import Path

def analyze(path):
    hours=Counter(); statuses=Counter(); paths=Counter(); durations=[]
    with open(path, encoding='utf-8', newline='') as f:
        for row in csv.DictReader(f):
            try:
                hour=int(row['timestamp'][11:13]); status=int(row['status']); duration=int(row['response_ms'])
                if not 0 <= hour <= 23 or not 100 <= status <= 599 or duration < 0: raise ValueError('out of range')
                hours[hour]+=1; statuses[status]+=1; paths[row['path']]+=1; durations.append(duration)
            except (ValueError, KeyError) as exc: raise ValueError(f'Invalid row at line {f.line_num}: {exc}') from exc
    if not durations: raise ValueError('No data rows found')
    total=len(durations); errors=sum(n for code,n in statuses.items() if code>=400)
    return {'requests':total,'errors_4xx_5xx':errors,'error_rate_percent':round(errors*100/total,2),'mean_response_ms':round(sum(durations)/total,2),'status_counts':dict(sorted(statuses.items())),'hourly_requests':{str(h).zfill(2):hours[h] for h in range(24)},'peak_hours_utc':[f'{h:02d}:00' for h in range(24) if hours[h]==max(hours.values())],'path_counts':dict(paths)}

def chart(values, title, output):
    maximum=max(values.values()) or 1; width=960; height=360; left=45; base=300; step=880/len(values); bars=[]
    for i,(label,value) in enumerate(values.items()):
        x=left+i*step; h=240*value/maximum
        bars.append(f'<rect x="{x:.1f}" y="{base-h:.1f}" width="{step*0.7:.1f}" height="{h:.1f}" fill="#2864a0"/><text x="{x:.1f}" y="{base+16}" font-size="10">{label}</text><text x="{x:.1f}" y="{base-h-4:.1f}" font-size="10">{value}</text>')
    output.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"><rect width="100%" height="100%" fill="white"/><text x="45" y="25" font-size="18">{title}</text>'+''.join(bars)+'</svg>',encoding='utf-8')

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input',type=Path,default=Path(__file__).with_name('server_logs.csv')); p.add_argument('--output',type=Path,default=Path(__file__).with_name('output')); a=p.parse_args()
    try:
        result=analyze(a.input); a.output.mkdir(parents=True,exist_ok=True)
        (a.output/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        chart(result['hourly_requests'],'Requests by hour (UTC)',a.output/'hourly.svg'); chart(result['status_counts'],'Requests by HTTP status',a.output/'statuses.svg')
        print(json.dumps(result,indent=2)); print('Graphs and summary written to',a.output)
    except (OSError, ValueError, csv.Error) as exc: raise SystemExit(f'Analysis failed: {exc}')
if __name__=='__main__': main()
