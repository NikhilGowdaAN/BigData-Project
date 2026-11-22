from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent

def main():
    d=pd.read_csv(ROOT/'sales.csv', parse_dates=['sale_date']); required={'sale_date','product','branch','quantity','unit_price'}
    if not required.issubset(d): raise ValueError(f'Missing columns: {required-set(d.columns)}')
    for c in ('quantity','unit_price'): d[c]=pd.to_numeric(d[c],errors='raise')
    if d[list(required)].isna().any().any() or (d[['quantity','unit_price']]<=0).any().any(): raise ValueError('Invalid sales row')
    d['revenue']=d.quantity*d.unit_price
    p=d.groupby('product')[['quantity','revenue']].sum().sort_values('revenue'); b=d.groupby('branch')[['quantity','revenue']].sum(); m=d.pivot_table(index='product',columns='branch',values='quantity',aggfunc='sum',fill_value=0)
    assert d.revenue.sum()==49951 and d.quantity.sum()==600 and p.revenue.sum()==b.revenue.sum()==49951
    out=ROOT/'graphs';out.mkdir(exist_ok=True)
    def save(fig,name):
        fig.tight_layout()
        for ext in ('png','svg'):fig.savefig(out/f'{name}.{ext}',dpi=300,bbox_inches='tight')
        plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,5)); bars=ax.barh(p.index,p.revenue,color=['#6391ac']*5+['#d47934']);ax.bar_label(bars,labels=[f'{v:,.0f} ({v/d.revenue.sum():.1%})' for v in p.revenue],padding=4);ax.set(xlabel='Revenue (currency units)',title='Product revenue and share of total');ax.set_xlim(0,p.revenue.max()*1.36);save(fig,'fig_1_1_product_contribution')
    fig,axes=plt.subplots(1,2,figsize=(10,4.6));
    for ax,c,title,y in zip(axes,['revenue','quantity'],['A. Revenue','B. Units sold'],['Revenue (currency units)','Units']):
        s=b[c].reindex(['South','West','North']);bars=ax.bar(s.index,s.values,color=['#d47934','#397c9f','#82a8bb']);ax.bar_label(bars,fmt='%.0f',padding=3);ax.set(title=title,ylabel=y);ax.set_ylim(0,s.max()*1.2)
    save(fig,'fig_1_2_branch_comparison')
    fig,ax=plt.subplots(figsize=(8,5));im=ax.imshow(m.values,cmap='Blues');ax.set_xticks(range(len(m.columns)),m.columns);ax.set_yticks(range(len(m.index)),m.index);ax.set(xlabel='Branch',ylabel='Product',title='Units sold by product and branch');
    for i in range(len(m.index)):
        for j in range(len(m.columns)):ax.text(j,i,str(m.iloc[i,j]),ha='center',va='center',color='white' if m.iloc[i,j]>m.to_numpy().max()/2 else 'black')
    fig.colorbar(im,ax=ax,label='Units sold');save(fig,'fig_1_3_branch_demand')
    daily=d.groupby('sale_date').revenue.sum().sort_index();fig,ax=plt.subplots(figsize=(10,4.5));ax.plot(daily.index,daily.values,marker='o',color='#276c91');peak=daily.idxmax();ax.annotate(f'Peak: {daily.max():,.0f}',(peak,daily.max()),xytext=(0,12),textcoords='offset points',ha='center');ax.set(title='Daily sales revenue',xlabel='Sale date (2025)',ylabel='Revenue (currency units)');ax.grid(alpha=.2);fig.autofmt_xdate();save(fig,'fig_1_4_daily_revenue')
    result=ROOT/'outputs';result.mkdir(exist_ok=True);p.assign(revenue_share_pct=p.revenue/d.revenue.sum()*100).sort_values('revenue',ascending=False).to_csv(result/'product_summary.csv');b.assign(revenue_share_pct=b.revenue/d.revenue.sum()*100).to_csv(result/'branch_summary.csv');print('PASS: 600 units, 49,951 revenue; summary tables and figures generated')
if __name__=='__main__':main()
