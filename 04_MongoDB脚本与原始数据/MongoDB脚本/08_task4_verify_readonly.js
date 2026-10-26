// Run with libReader authentication after restarting mongod with --auth
const d=db.getSiblingDB('library');
print('=== S3 read-only user validation ===');
print('read books count='+d.books.countDocuments({}));
try { d.books.insertOne({isbn:'TEST_SHOULD_FAIL',title:'permission_test'});print('UNEXPECTED: write succeeded'); }
catch(e){print('EXPECTED write denied: '+e.code+' '+e.codeName);}
