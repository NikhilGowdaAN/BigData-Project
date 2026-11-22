import csv,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class GraphEvidenceTest(unittest.TestCase):
 def test_hive_reconciliation(self):
  with (ROOT/'01_Hive/sales.csv').open(newline='') as f: rows=list(csv.DictReader(f))
  self.assertEqual(sum(int(x['quantity']) for x in rows),600)
  self.assertEqual(sum(int(x['quantity'])*float(x['unit_price']) for x in rows),49951)
  self.assertEqual(sum(int(x['quantity'])*float(x['unit_price']) for x in rows if x['branch']=='South'),20150)
 def test_kafka_capture(self):
  path=ROOT/'02_Kafka/outputs/traffic_events.csv'
  if not path.exists(): self.skipTest('No Kafka capture')
  with path.open(newline='') as f: rows=list(csv.DictReader(f))
  self.assertTrue(rows)
  for r in rows:self.assertEqual(r['congestion_alert'].lower()=='true',float(r['speed_kmh'])<25 and int(r['vehicles'])>=30)
 def test_flink_runtime(self):
  path=ROOT/'03_Flink/outputs/flink_run.log'
  if not path.exists():self.skipTest('No Flink log')
  text=path.read_text(encoding='utf-8');self.assertEqual(text.count(' | READING '),60);self.assertEqual(text.count(' | ALERT '),34);self.assertEqual(text.count(' | SUMMARY '),18)
 def test_catalog(self):
  data=json.loads((ROOT/'04_MongoDB/products.json').read_text());self.assertEqual(len(data),24);self.assertEqual(len({x['sku'] for x in data}),24);self.assertTrue(all(x['price']>=0 and x['stock']>=0 for x in data))
 def test_cloud(self):
  with (ROOT/'05_Cloud_Analytics/server_logs.csv').open(newline='') as f: rows=list(csv.DictReader(f))
  self.assertEqual(len(rows),480);self.assertEqual(sum(int(r['status'])>=400 for r in rows),29)
 def test_generated_files(self):
  names={'01_Hive':['fig_1_1_product_contribution','fig_1_2_branch_comparison','fig_1_3_branch_demand','fig_1_4_daily_revenue'],'02_Kafka':['fig_2_1_sensor_time','fig_2_2_alerts_by_sensor','fig_2_3_volume_speed','fig_2_4_event_status'],'03_Flink':['01_vital_signs_over_time','02_threshold_alerts','03_window_aggregations','04_reading_classification'],'04_MongoDB':['01_products_by_category','02_average_price_by_category','03_stock_by_category','04_price_vs_stock'],'05_Cloud_Analytics':['fig_5_1_status','fig_5_2_hourly','fig_5_3_endpoints','fig_5_4_errors']}
  for folder,files in names.items():
   for name in files:
    for ext in ('png','svg'):
     path=ROOT/folder/'graphs'/f'{name}.{ext}'
     with self.subTest(path=path):self.assertTrue(path.is_file() and path.stat().st_size>0,str(path))
 def test_reports(self):
  headings=['Activity Name','Problem Definition','Objectives','Technology Study','Architecture and Working','Implementation and Procedure','Code, Queries and Configurations','Outputs, Graphs and Images','Analysis and Interpretation','Limitations','Conclusion']
  for folder in ['01_Hive','02_Kafka','03_Flink','04_MongoDB','05_Cloud_Analytics']:
   text=(ROOT/folder/'REPORT.md').read_text(encoding='utf-8')
   for i,heading in enumerate(headings,1):self.assertIn(f'# {i}. {heading}',text)
if __name__=='__main__':unittest.main()
