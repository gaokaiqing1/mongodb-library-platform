// I1-I5; execute with mongosh localhost:27017; no collection deletion.
const d=db.getSiblingDB('library');const b=d.books;
const filter={category:'计算机',price:{$gt:50}};
const summary=(e)=>({nReturned:e.executionStats.nReturned,totalDocsExamined:e.executionStats.totalDocsExamined,totalKeysExamined:e.executionStats.totalKeysExamined,executionTimeMillis:e.executionStats.executionTimeMillis,winningPlan:e.queryPlanner.winningPlan});
print('=== [I0] BEFORE INDEXES: BASELINE ===');
printjson({books:b.countDocuments({}),readers:d.readers.countDocuments({}),borrow_logs:d.borrow_logs.countDocuments({})});
// Hint natural performs a full scan even on repeated runs; isolates scan baseline.
printjson(summary(b.find(filter).hint({$natural:1}).explain('executionStats')));
print('=== [I1-I5] CREATE INDEXES ===');
for(const spec of [{id:'I1',key:{isbn:1},options:{unique:true,name:'idx_isbn_unique'}},{id:'I2',key:{title:1},options:{name:'idx_title'}},{id:'I3',key:{category:1},options:{name:'idx_category'}},{id:'I4',key:{tags:1},options:{name:'idx_tags'}},{id:'I5',key:{category:1,price:1},options:{name:'idx_category_price'}}]){
  const name=b.createIndex(spec.key,spec.options);print(spec.id+' CREATED/EXISTS: '+name);
}
print('=== [I6] getIndexes() ===');
for(const i of b.getIndexes()) printjson({name:i.name,key:i.key,unique:i.unique===true});
print('=== [I7] MULTIKEY CHECK ===');
const tagExp=b.find({tags:'编程'}).hint('idx_tags').explain('executionStats');
printjson({nReturned:tagExp.executionStats.nReturned,totalKeysExamined:tagExp.executionStats.totalKeysExamined,indexName:'idx_tags'});
print('=== [I8] AFTER: COMPOUND INDEX EXPLAIN ===');
printjson(summary(b.find(filter).hint('idx_category_price').explain('executionStats')));
print('=== [I9] UNIQUE ISBN DUPLICATE INSERT TEST ===');
try{b.insertOne({isbn:'9787115428028',title:'TEST-DUPLICATE-DO-NOT-KEEP',price:1});print('FAILED: duplicate was accepted');}
catch(e){print('EXPECTED E11000: '+e.code+' '+e.codeName);}
print('=== [I10] FINAL COUNTS ===');
printjson({books:b.countDocuments({}),readers:d.readers.countDocuments({}),borrow_logs:d.borrow_logs.countDocuments({}),category_stats:d.category_stats.countDocuments({})});
