// Requires dbAdmin (collMod) privilege on library. No drop/rebuild.
const d=db.getSiblingDB('library');
const info=d.getCollectionInfos({name:'borrow_logs'})[0];
if(!info || info.type!=='timeseries') throw Error('STOP: expected time-series borrow_logs');
const old=Number(info.options.expireAfterSeconds);
print('TTL BEFORE = '+old);
if(old!==157680000) {
  const result=d.runCommand({collMod:'borrow_logs',expireAfterSeconds:157680000});
  print('COLLMOD '+EJSON.stringify(result));
  if(result.ok!==1) throw Error('collMod failed; administrator permission required');
}
const next=d.getCollectionInfos({name:'borrow_logs'})[0];
print('TTL AFTER = '+next.options.expireAfterSeconds);
if(Number(next.options.expireAfterSeconds)!==157680000) throw Error('TTL verification failed');
print('PASS TTL FIVE YEARS');
