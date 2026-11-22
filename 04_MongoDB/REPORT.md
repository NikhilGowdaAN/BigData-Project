# 1. Activity Name

MongoDB: E-Commerce Product Catalog.

# 2. Problem Definition

A product catalog needs to store and retrieve product attributes and update inventory. Product attributes can vary by category; a document model permits related attributes and arrays to be stored together. This exercise prepares an isolated catalog demonstration.

# 3. Objectives

1. Analyze the supplied product JSON.
2. Group products by category.
3. Compare prices and stock.
4. Prepare create, read, update and delete operations.
5. Prepare indexes and query plan inspection.
6. Compare document and relational representations.

# 4. Technology Study

MongoDB stores BSON documents in collections. Flexible document fields and nested arrays support varying product attributes; schema validation may be configured where consistency is needed. Indexes improve selected lookups at the cost of storage and write overhead. Query plans reveal optimizer choices. Unlike a normalized relational design, tags can be embedded in a document instead of requiring a separate join table. Both approaches can support constraints and transactions; suitability depends on access patterns.

# 5. Architecture and Working

See [architecture.mmd](architecture.mmd). JSON is analyzed locally for plots. A separate mongosh script can load the dedicated assignment collection, perform CRUD, create indexes and show a plan. Compass can inspect that same collection. The plotting workflow does not connect to MongoDB.

# 6. Implementation and Procedure

The dataset contains 24 synthetic product documents with SKU, name, category, price, stock, tags and active flag. Generate figures using `python 04_MongoDB/graphs.py`. Live CRUD remains pending at the user's instruction. When authorized, run `.\04_MongoDB\run.ps1`; its setup deletes and reloads the dedicated assignment products collection.

# 7. Code, Queries and Configurations

[operations.js](operations.js) inserts documents, filters electronics, increments a demo item's stock, deletes it, and creates unique SKU and compound category/price indexes. The script inspects `explain('executionStats')`; actual index selection depends on data and optimizer behavior. [graphs.py](graphs.py) reads JSON directly.

# 8. Outputs, Graphs and Images

All figures use [products.json](products.json), not a live database query.

1. [Figure 4.1: category counts](graphs/01_products_by_category.png) shows six products in each category.
2. [Figure 4.2: average prices](graphs/02_average_price_by_category.png) compares arithmetic category means.
3. [Figure 4.3: category stock](graphs/03_stock_by_category.png) compares summed units.
4. [Figure 4.4: price versus stock](graphs/04_price_vs_stock.png) uses existing fields because ratings are absent.

Capture actual CRUD and Compass results later using [SCREENSHOTS.md](SCREENSHOTS.md).

# 9. Analysis and Interpretation

| Category | Products | Mean price | Stock units |
|---|---:|---:|---:|
| Accessories | 6 | 484 | 134 |
| Electronics | 6 | 519 | 94 |
| Stationery | 6 | 554 | 136 |
| Home | 6 | 589 | 96 |

Electronics has the lowest total stock in this synthetic sample. Restocking decisions require actual demand and supplier lead times; category totals alone are insufficient.

# 10. Limitations

The catalog is synthetic and small; it contains no ratings or real demand. MongoDB connection and CRUD were not executed in this phase. The JSON-derived graphs do not prove live database state or index performance.

# 11. Conclusion

The local catalog analysis and CRUD scripts are prepared. A genuine MongoDB execution and screenshots remain pending until the user chooses to run them.
