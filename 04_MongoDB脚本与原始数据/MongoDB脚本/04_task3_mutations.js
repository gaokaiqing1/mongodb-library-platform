// 04_task3_mutations.js | runs against task-specific copy; original library untouched
// Xshell: mongosh "mongodb://127.0.0.1:27017" 04_task3_mutations.js
const original=db.getSiblingDB('library');const lab=db.getSiblingDB('library_task3');
function init(name){let docs=original.getCollection(name).find().toArray();if(lab.getCollectionNames().includes(name))lab.getCollection(name).drop();if(name==='borrow_logs')name='borrow_logs_ops';lab.getCollection(name).insertMany(docs);print('COPY '+name+' count='+lab.getCollection(name).countDocuments({}));}
print('=== CREATE FRESH TASK3 ISOLATED COPIES ===');init('books');init('readers');init('borrow_logs');
const b=lab.books, r=lab.readers, logs=lab.borrow_logs_ops;
function show(label,result){print(label);printjson({matchedCount:result.matchedCount,modifiedCount:result.modifiedCount,deletedCount:result.deletedCount});}
print('\n[U1] 减少库存5（选择stock=15的Python书）');show('U1',b.updateOne({isbn:'9787115428028',stock:{$gte:5}},{$inc:{stock:-5}}));printjson(b.findOne({isbn:'9787115428028'},{_id:0,title:1,stock:1}));
print('\n[U2] 数学类价格打九折');show('U2',b.updateMany({category:'数学'},{$mul:{price:0.9}}));printjson(b.find({category:'数学'},{_id:0,title:1,price:1}).toArray());
print('\n[U3] currentDate字段');show('U3',b.updateOne({isbn:'9787115428028'},{$currentDate:{last_modified:true}}));printjson(b.findOne({isbn:'9787115428028'},{_id:0,title:1,last_modified:1}));
print('\n[U4] unset tags');show('U4',b.updateOne({isbn:'9787115428028'},{$unset:{tags:''}}));printjson(b.findOne({isbn:'9787115428028'},{_id:0,title:1,tags:1}));
print('\n[D1] on ordinary copy because deleteOne is not supported for time-series collections');let target=logs.findOne({status:{$eq:'已归还'}});print('preview:');printjson(target);show('D1',logs.deleteOne({_id:target._id,status:{$eq:'已归还'}}));
print('\n[D2] Preview status=逾期 and return_date missing (actual overdue unpaid definition)');let f={status:'逾期',return_date:{$exists:false}};print('preview-count='+logs.countDocuments(f));printjson(logs.find(f,{_id:0,reader_card:1,book_isbn:1,status:1}).toArray());show('D2',logs.deleteMany(f));print('note: supplied dataset overdue entries have return_date; expected 0 deleted');
print('\n[D3] replace reader while retaining _id');let prev=r.findOne({card_no:'R20240001'});let {_id,...fields}=prev;let replacement={...fields,phone:'13800138099',level:'高级'};show('D3',r.replaceOne({_id:prev._id},replacement));printjson(r.findOne({_id:prev._id},{_id:1,card_no:1,name:1,phone:1,level:1}));
print('\nISOLATED COUNTS');printjson({books:b.countDocuments({}),readers:r.countDocuments({}),borrow_logs_ops:logs.countDocuments({})});
print('ORIGINAL COUNTS');printjson({books:original.books.countDocuments({}),readers:original.readers.countDocuments({}),borrow_logs:original.borrow_logs.countDocuments({})});
