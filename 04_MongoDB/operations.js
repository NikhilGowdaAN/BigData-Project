// Run with mongosh <URI> --file 04_MongoDB/operations.js. Uses only a dedicated demo database.
const fs = require('fs');
const path = require('path');
const demo = db.getSiblingDB('big_data_assignment_catalog');
const products = JSON.parse(fs.readFileSync(path.join(__dirname, 'products.json'), 'utf8'));
const collection = demo.products;
// Repeatable setup: replace only this assignment collection.
collection.deleteMany({});
collection.insertMany(products);
collection.createIndex({sku: 1}, {unique: true});
collection.createIndex({category: 1, price: 1});
print('COUNT AFTER IMPORT: ' + collection.countDocuments());
print('READ ELECTRONICS:'); printjson(collection.find({category:'Electronics'}, {_id:0, sku:1, name:1, price:1}).sort({price:1}).toArray());
print('CREATE:'); printjson(collection.insertOne({sku:'DEMO-NEW', name:'Demo Keyboard', category:'Electronics', price:899, stock:10, active:true}));
print('UPDATE:'); printjson(collection.updateOne({sku:'DEMO-NEW'}, {$inc:{stock:5}}));
print('UPDATED DOCUMENT:'); printjson(collection.findOne({sku:'DEMO-NEW'}, {_id:0}));
print('DELETE:'); printjson(collection.deleteOne({sku:'DEMO-NEW'}));
print('INDEXES:'); printjson(collection.getIndexes());
print('QUERY PLAN:'); printjson(collection.find({category:'Electronics'}).sort({price:1}).explain('executionStats').queryPlanner.winningPlan);
