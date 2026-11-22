import csv, importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
class ProjectsTest(unittest.TestCase):
    def test_sales(self):
        with (ROOT/'01_Hive/sales.csv').open(newline='') as f: rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),120); self.assertTrue(all(int(r['quantity'])>0 and float(r['unit_price'])>0 for r in rows)); self.assertEqual(len({r['sale_id'] for r in rows}),120)
    def test_traffic(self):
        c=load('traffic',ROOT/'02_Kafka/common.py'); self.assertTrue(c.classify({'speed_kmh':24,'vehicles':30})); self.assertFalse(c.classify({'speed_kmh':25,'vehicles':30})); self.assertFalse(c.classify({'speed_kmh':24,'vehicles':29})); self.assertRaises(ValueError,c.decode,'[]')
    def test_catalog(self):
        p=json.loads((ROOT/'04_MongoDB/products.json').read_text()); self.assertEqual(len(p),24); self.assertEqual(len({x['sku'] for x in p}),24); self.assertTrue(all(x['price']>0 and x['stock']>=0 for x in p))
    def test_logs(self):
        a=load('analysis',ROOT/'05_Cloud_Analytics/analysis.py'); result=a.analyze(ROOT/'05_Cloud_Analytics/server_logs.csv'); self.assertEqual(result['requests'],480); self.assertEqual(sum(result['hourly_requests'].values()),480); self.assertEqual(len(result['peak_hours_utc']),24); self.assertEqual(result['errors_4xx_5xx'],29)
if __name__=='__main__': unittest.main()
