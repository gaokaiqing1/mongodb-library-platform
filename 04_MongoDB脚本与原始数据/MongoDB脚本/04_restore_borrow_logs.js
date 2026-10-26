// Safe idempotent restore of only missing original records. Run as libWriter.
// Run from /root/library_project, with borrow_logs.txt next to script.
const fs=require('fs');const path=require('path');
const d=db.getSiblingDB('library');
const info=d.getCollectionInfos({name:'borrow_logs'})[0];
if(!info || info.type!=='timeseries') throw Error('STOP: not a time-series collection');
if(Number(info.options.expireAfterSeconds)!==157680000) throw Error('STOP: TTL is not five years. Run 03_set_borrow_logs_ttl.js first');
const raw=fs.readFileSync(path.join(process.cwd(),'borrow_logs.txt'),'utf8').replace(/^\uFEFF/,'');
const expected=EJSON.parse(raw);
if(!Array.isArray(expected)||expected.length!==66) throw Error('STOP: source borrow_logs.txt must have exactly 66 records');
function ts(x){return x instanceof Date?x.toISOString():x==null?'':String(x);}
function key(x){return JSON.stringify([ts(x.borrow_date),x.reader_card,x.book_isbn,x.status,ts(x.return_date)]);}
const wanted=new Map();for(const row of expected){if(!(row.borrow_date instanceof Date))throw Error('STOP: invalid borrow_date');const k=key(row);if(wanted.has(k))throw Error('STOP: source has duplicate records');wanted.set(k,row);}
const current=d.borrow_logs.find().toArray();const have=new Set();
for(const row of current){const k=key(row);if(!wanted.has(k))throw Error('STOP: DB contains records outside supplied historical dataset. Do not overwrite live data.');if(have.has(k))throw Error('STOP: duplicate rows already present');have.add(k);}
const missing=[...wanted].filter(([k])=>!have.has(k)).map(([,row])=>row);
print('BEFORE='+current.length+' SOURCE='+expected.length+' MISSING='+missing.length);
if(missing.length){const r=d.borrow_logs.insertMany(missing,{ordered:true});print('INSERTED='+Object.keys(r.insertedIds).length);}else print('INSERTED=0');
const after=d.borrow_logs.find().toArray();
const afterKeys=new Set(after.map(key));
if(after.length!==66||afterKeys.size!==66||[...wanted.keys()].some(k=>!afterKeys.has(k))) throw Error('FINAL CHECK FAILED: counts or identities differ');
print('AFTER='+after.length);
print('PASS: 66 historical borrowing records restored and verified');
