// 06_task4_indexes.js: I1-I5, repeatable; explain for small dataset is NOT proof of speedup
const d=db.getSiblingDB('library'),b=d.books;
print('=== explain BEFORE new indexes ===');
let filter={category:'计算机',price:{$gt:50}};
let before=b.find(filter).explain('executionStats');printjson({winningPlan:before.queryPlanner.winningPlan,executionStats:{nReturned:before.executionStats.nReturned,totalDocsExamined:before.executionStats.totalDocsExamined,executionTimeMillis:before.executionStats.executionTimeMillis}});
print('=== create I1-I5 ===');
print('I1='+b.createIndex({isbn:1},{unique:true,name:'idx_isbn_unique'}));
print('I2='+b.createIndex({title:1},{name:'idx_title'}));
print('I3='+b.createIndex({category:1},{name:'idx_category'}));
print('I4='+b.createIndex({tags:1},{name:'idx_tags'}));
print('I5='+b.createIndex({category:1,price:1},{name:'idx_category_price'}));
print('INDEX LIST');printjson(b.getIndexes());
print('=== explain AFTER (index hint to display planned path; compare docs examined) ===');
let after=b.find(filter).hint('idx_category_price').explain('executionStats');printjson({winningPlan:after.queryPlanner.winningPlan,executionStats:{nReturned:after.executionStats.nReturned,totalDocsExamined:after.executionStats.totalDocsExamined,executionTimeMillis:after.executionStats.executionTimeMillis}});
print('=== I1 DUPLICATE ISBN TEST ===');
try{b.insertOne({isbn:'9787115428028',title:'索引重复检测_应失败',author:'TEST',price:1,stock:1,rating:5});print('ERROR: duplicate succeeded unexpectedly');}catch(e){print('EXPECTED duplicate key rejection: '+e.code+' '+e.codeName);}
print('books count='+b.countDocuments({}));
