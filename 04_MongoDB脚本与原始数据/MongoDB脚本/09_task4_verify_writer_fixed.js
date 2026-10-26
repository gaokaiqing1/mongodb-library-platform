const d=db.getSiblingDB('library');const c=d.book_logs;
print('=== [S3] WRITER READ TEST ===');print('books='+d.books.countDocuments({}));
print('=== [S3] WRITER WRITE TEST ON book_logs (NOT original books) ===');
let id=null;
try{const x=c.insertOne({event:'role_validation',created_at:new Date()});id=x.insertedId;print('insert acknowledged='+x.acknowledged);}
finally{if(id){const r=c.deleteOne({_id:id});print('cleanup deletedCount='+r.deletedCount);}}
print('=== [S3] FINISHED ===');
