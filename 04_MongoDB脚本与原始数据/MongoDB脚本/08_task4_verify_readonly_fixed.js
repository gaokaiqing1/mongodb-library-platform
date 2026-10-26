const d=db.getSiblingDB('library');
print('=== [S3] READONLY READ TEST ===');print('books='+d.books.countDocuments({}));
print('=== [S3] READONLY WRITE DENIAL TEST ===');
try{d.books.insertOne({isbn:'TEST_SHOULD_NOT_WRITE',title:'permission_check'});print('UNEXPECTED WRITE SUCCEEDED - STOP AND REVIEW');}
catch(e){print('EXPECTED DENIED: '+e.code+' '+e.codeName);}
