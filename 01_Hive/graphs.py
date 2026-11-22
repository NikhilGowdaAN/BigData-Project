from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

ROOT = Path(__file__).resolve().parent

def main():
    df = pd.read_csv(ROOT / 'sales.csv')
    required = {'branch', 'product', 'quantity', 'unit_price'}
    if not required.issubset(df.columns):
        raise ValueError(f'Missing columns: {required - set(df.columns)}')
    for c in ('quantity', 'unit_price'):
        df[c] = pd.to_numeric(df[c], errors='raise')
        if df[c].isna().any() or (df[c] <= 0).any(): raise ValueError(f'Invalid {c}')
    if df[['branch','product']].isna().any().any(): raise ValueError('Missing branch or product')
    df['revenue'] = df.quantity * df.unit_price
    products = df.groupby('product')[['quantity','revenue']].sum()
    branches = df.groupby('branch')[['quantity','revenue']].sum()
    matrix = df.pivot_table(index='product', columns='branch', values='quantity', aggfunc='sum', fill_value=0)
    expected_p = {'Tea':(121,19360), 'Apples':(108,12960), 'Rice':(90,5850), 'Milk':(117,5616), 'Bread':(85,3400), 'Soap':(79,2765)}
    expected_b = {'South':(203,20150), 'West':(240,19038), 'North':(157,10763)}
    assert df.revenue.sum() == 49951 and all(tuple(products.loc[k]) == v for k,v in expected_p.items()) and all(tuple(branches.loc[k]) == v for k,v in expected_b.items()), 'Sales no longer match supplied Hive totals'
    out = ROOT / 'graphs'; out.mkdir(exist_ok=True)
    def save(fig, name):
        fig.tight_layout()
        for ext in ('png','svg'): fig.savefig(out / f'{name}.{ext}', dpi=300, bbox_inches='tight')
        plt.close(fig)
    def bars(series, title, ylabel, name):
        fig, ax = plt.subplots(figsize=(9,5)); bars = ax.bar(series.index,series.values,color=plt.cm.viridis([.2,.3,.4,.5,.6,.7][:len(series)]))
        ax.bar_label(bars, fmt='%.0f', padding=3); ax.set(title=title,ylabel=ylabel,xlabel='Product' if 'product' in name else 'Branch'); ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')); ax.set_ylim(0,max(series)*1.16); ax.grid(axis='y',alpha=.2); ax.set_axisbelow(True); save(fig,name)
    bars(products.revenue.sort_values(ascending=False),'Product revenue','Revenue (currency units)','01_product_revenue')
    bars(branches.revenue.reindex(['South','West','North']),'Branch revenue','Revenue (currency units)','02_branch_revenue')
    bars(products.quantity.sort_values(ascending=False),'Product demand','Units sold','03_product_units')
    fig,ax=plt.subplots(figsize=(11,6)); matrix.plot.bar(ax=ax, rot=0, color=['#245a81','#db8242','#5b8c5a']);
    for container in ax.containers: ax.bar_label(container, padding=2, fontsize=8)
    ax.set(title='Product demand by branch',xlabel='Product',ylabel='Units sold'); ax.legend(title='Branch'); ax.set_ylim(0,matrix.to_numpy().max()*1.2); ax.grid(axis='y',alpha=.2); ax.set_axisbelow(True); save(fig,'04_branch_product_units')
    print('PASS: supplied product, branch and total figures match CSV; generated eight files in',out)
    print(matrix.to_string())
if __name__ == '__main__': main()
