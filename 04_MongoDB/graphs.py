from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent

def main():
    d=pd.read_json(ROOT/'products.json'); required={'category','price','stock'}
    if not required.issubset(d):raise ValueError(f'Missing columns: {required-set(d.columns)}')
    for c in ['price','stock']:d[c]=pd.to_numeric(d[c],errors='raise')
    if d[list(required)].isna().any().any() or (d[['price','stock']]<0).any().any():raise ValueError('Invalid catalog values')
    charts=[('01_products_by_category','Products by category','Products',d.groupby('category').size()),('02_average_price_by_category','Average price by category','Average price (currency units)',d.groupby('category').price.mean()),('03_stock_by_category','Stock by category','Stock units',d.groupby('category').stock.sum()),('04_price_vs_stock','Product price and stock','Stock units',None)]
    out=ROOT/'graphs';out.mkdir(exist_ok=True)
    for name,title,y,s in charts:
        fig,ax=plt.subplots(figsize=(9,5))
        if s is None:
            for category,g in d.groupby('category'):ax.scatter(g.price,g.stock,label=category,s=45)
            ax.set_xlabel('Price (currency units)');ax.legend(title='Category');ax.set_ylabel(y)
        else:
            b=ax.bar(s.index,s.values,color='#286491');ax.bar_label(b,fmt='%.1f' if 'average' in name else '%.0f',padding=3);ax.set_ylim(0,max(s)*1.18);ax.set(xlabel='Category',ylabel=y)
        ax.set_title(title);ax.grid(axis='y',alpha=.2);fig.tight_layout()
        for ext in ('png','svg'):fig.savefig(out/f'{name}.{ext}',dpi=300,bbox_inches='tight')
        plt.close(fig)
    print(f'{len(d)} catalog documents; charts in {out}; no database connection made')
if __name__=='__main__':main()
