// Put books.txt, readers.txt, borrow_logs.txt alongside this script on Linux.
// Run: mongosh "mongodb://127.0.0.1:27017" 02_import_dataset.js
// The script checks for existing data and will not duplicate records.
const fs = require('fs');
const path = require('path');
const base = process.cwd();
const library = db.getSiblingDB('library');
function load(filename) {
  const raw = fs.readFileSync(path.join(base,filename),'utf8').replace(/^\uFEFF/,'');
  const data = EJSON.parse(raw);
  if(!Array.isArray(data)) throw new Error(filename + ' is not a JSON array');
  return data;
}
function importCollection(filename, collectionName) {
  const arr = load(filename);
  const coll = library.getCollection(collectionName);
  const existing = coll.countDocuments({});
  if (existing !== 0) {
    print('SKIP ' + collectionName + ': existing=' + existing + ', to prevent duplicate import');
    return;
  }
  if (!arr.length) throw new Error('Empty input: '+filename);
  print('INSERT ONE into ' + collectionName);
  printjson(coll.insertOne(arr[0]));
  if (arr.length > 1) {
    print('INSERT MANY ' + (arr.length-1) + ' into ' + collectionName);
    const res = coll.insertMany(arr.slice(1));
    printjson({acknowledged:res.acknowledged,insertedCount:Object.keys(res.insertedIds).length});
  }
  print('COUNT ' + collectionName + ' = ' + coll.countDocuments({}));
}
importCollection('books.txt','books');
importCollection('readers.txt','readers');
importCollection('borrow_logs.txt','borrow_logs');
print('EXPECTED baseline: books=20 readers=16 borrow_logs=66');
printjson({books:library.books.countDocuments({}),readers:library.readers.countDocuments({}),borrow_logs:library.borrow_logs.countDocuments({}),in_stock:library.book_in_stock.countDocuments({})});
