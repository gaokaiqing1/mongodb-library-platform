// Run while authentication is still OFF. Interactive password entry; no hard-coded passwords.
const d=db.getSiblingDB('library');
print('=== [S1] CREATE READONLY libReader ===');
if(d.getUser('libReader'))print('EXISTS: libReader (role changes not performed)');
else printjson(d.createUser({user:'libReader',pwd:passwordPrompt('libReader password: '),roles:[{role:'read',db:'library'}]}));
print('=== [S2] CREATE WRITER libWriter ===');
if(d.getUser('libWriter'))print('EXISTS: libWriter (role changes not performed)');
else printjson(d.createUser({user:'libWriter',pwd:passwordPrompt('libWriter password: '),roles:[{role:'readWrite',db:'library'},{role:'dbAdmin',db:'library'}]}));
print('=== [S2] USER ROLES; PASSWORDS ARE NOT DISPLAYED ===');
printjson(d.getUsers().users.filter(u=>['libReader','libWriter'].includes(u.user)).map(u=>({user:u.user,roles:u.roles})));
