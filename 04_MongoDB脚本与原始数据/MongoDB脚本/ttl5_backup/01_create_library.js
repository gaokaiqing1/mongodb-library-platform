// Run using: mongosh "mongodb://127.0.0.1:27017" 01_create_library.js
// Lab only. Safe to rerun: existing collections are preserved.
const lab = db.getSiblingDB('library');
function exists(name) { return lab.getCollectionInfos({name}).length > 0; }
for (const name of ['books','readers','category_stats']) {
  if (!exists(name)) { print('CREATE ' + name); printjson(lab.createCollection(name)); }
  else print('EXISTS ' + name);
}
if (!exists('book_logs')) {
  print('CREATE capped book_logs');
  printjson(lab.createCollection('book_logs',{capped:true,size:1048576,max:1000}));
}
if (!exists('borrow_logs')) {
  print('CREATE timeseries borrow_logs');
  printjson(lab.createCollection('borrow_logs', {
    timeseries:{timeField:'borrow_date',granularity:'hours'},
    expireAfterSeconds:63072000
  }));
}
if (!exists('book_in_stock')) {
  print('CREATE view book_in_stock');
  printjson(lab.createView('book_in_stock','books',[{$match:{stock:{$gt:0}}}]));
}
print('--- COLLECTION TYPES AND OPTIONS ---');
lab.getCollectionInfos().filter(x => ['books','readers','category_stats','book_logs','borrow_logs','book_in_stock'].includes(x.name))
  .forEach(x => printjson({name:x.name,type:x.type,options:x.options}));
