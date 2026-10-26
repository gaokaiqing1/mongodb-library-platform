// 03_task3_queries.js | Xshell: mongosh "mongodb://127.0.0.1:27017" 03_task3_queries.js
const d = db.getSiblingDB('library');
function run(id, description, collection, filter, projection){
  const col=d.getCollection(collection);
  const result=col.find(filter,projection||{}).toArray();
  print('\n['+id+'] '+description+' | count='+result.length);
  result.forEach(x=>print(EJSON.stringify(x)));
}
print('=== TASK 3: QUERIES (original library data, read only) ===');
run('Q1','price > 80','books',{price:{$gt:80}},{_id:0,title:1,price:1});
run('Q2','stock < 10','books',{stock:{$lt:10}},{_id:0,title:1,stock:1});
run('Q3','ISBN exact match','books',{isbn:{$eq:'9787115428028'}},{_id:0,title:1,isbn:1});
run('Q4','email null / absent','readers',{email:{$eq:null}},{_id:0,card_no:1,name:1,email:1});
run('Q5','publisher != 人民邮电出版社','books',{publisher:{$ne:'人民邮电出版社'}},{_id:0,title:1,publisher:1});
run('Q6','computer or management','books',{category:{$in:['计算机','经济管理']}},{_id:0,title:1,category:1});
run('Q7','computer rating > 4.0','books',{$and:[{category:'计算机'},{rating:{$gt:4.0}}]},{_id:0,title:1,rating:1});
run('Q8','rating < 3.5 or zero stock','books',{$or:[{rating:{$lt:3.5}},{stock:0}]},{_id:0,title:1,rating:1,stock:1});
run('Q9','title regex Python','books',{title:{$regex:'Python'}},{_id:0,title:1});
run('Q10','tags contain both 编程 and 入门','books',{tags:{$all:['编程','入门']}},{_id:0,title:1,tags:1});
run('Q11','tags exact size 3','books',{tags:{$size:3}},{_id:0,title:1,tags:1});
run('Q12','tags exists','books',{tags:{$exists:true}},{_id:0,title:1});
run('Q13','_id is string','books',{_id:{$type:'string'}},{title:1});
let top=d.books.find({}, {_id:0,title:1,rating:1}).sort({rating:-1,isbn:1}).limit(5).toArray();
print('\n[Q14] rating TOP 5 | count='+top.length);top.forEach(x=>print(EJSON.stringify(x)));
run('Q15','projection title price rating','books',{}, {_id:0,title:1,price:1,rating:1});
let cats=d.books.distinct('category').sort();print('\n[Q16] distinct category | count='+cats.length);printjson(cats);
print('\n=== BASELINE COUNTS ===');printjson({books:d.books.countDocuments({}),readers:d.readers.countDocuments({}),borrow_logs:d.borrow_logs.countDocuments({})});
