CREATE DATABASE IF NOT EXISTS supermarket;
USE supermarket;
DROP TABLE IF EXISTS sales;
CREATE TABLE sales (sale_id INT, sale_date STRING, branch STRING, product STRING, category STRING, quantity INT, unit_price DECIMAL(10,2))
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE
TBLPROPERTIES ('skip.header.line.count'='1');
LOAD DATA LOCAL INPATH '/workspace/sales.csv' OVERWRITE INTO TABLE sales;
SELECT 'TOTAL_REVENUE', SUM(quantity * unit_price) FROM sales;
SELECT product, SUM(quantity) AS units, SUM(quantity * unit_price) AS revenue FROM sales GROUP BY product ORDER BY revenue DESC;
SELECT branch, SUM(quantity) AS units, SUM(quantity * unit_price) AS revenue FROM sales GROUP BY branch ORDER BY revenue DESC;
SELECT branch, product, SUM(quantity) AS units FROM sales GROUP BY branch, product ORDER BY branch, units DESC;
