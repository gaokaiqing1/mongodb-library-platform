// Safe read-only backup & inspection, run as libWriter on library.
const fs=require('fs');
const d=db.getSiblingDB('library');
const info=d.getCollectionInfos({name:'borrow_logs'})[0];
if(!info || info.type!=='timeseries') throw Error('STOP: borrow_logs is not a time-series collection');
const rows=d.borrow_logs.find().toArray();
const stamp=(new Date()).toISOString().replace(/[:.]/g,'-');
const filename='borrow_logs_before_ttl5_'+stamp+'.json';
fs.writeFileSync(filename,EJSON.stringify(rows,null,2),'utf8');
print('BACKUP '+filename+' count='+rows.length);
print('COLLECTION '+EJSON.stringify({type:info.type,options:info.options}));
print('ORIGINAL '+EJSON.stringify({books:d.books.countDocuments({}),readers:d.readers.countDocuments({}),borrow_logs:rows.length}));
