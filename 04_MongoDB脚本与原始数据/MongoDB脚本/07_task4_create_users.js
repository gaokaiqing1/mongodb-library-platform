// Run before enabling --auth; this is an idempotent demonstration for a local lab instance.
// Do not place real passwords in scripts. User prompted for password interactively by shell.
const d=db.getSiblingDB('library');
print('=== S1/S2: CREATE/VERIFY LAB USERS ===');
if(d.getUser('libReader'))print('libReader exists; no changes');
else {let p=passwordPrompt('请为 libReader 输入密码: ');printjson(d.createUser({user:'libReader',pwd:p,roles:[{role:'read',db:'library'}]}));}
if(d.getUser('libWriter'))print('libWriter exists; no changes');
else {let p=passwordPrompt('请为 libWriter 输入密码: ');printjson(d.createUser({user:'libWriter',pwd:p,roles:[{role:'readWrite',db:'library'},{role:'dbAdmin',db:'library'}]}));}
printjson(d.getUsers().users.map(x=>({user:x.user,roles:x.roles})));
