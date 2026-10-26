// 05_task4_aggregation.js 任务四 A1-A9，始终基于原始 library
const d=db.getSiblingDB('library');
function out(id,desc,col,pipeline){print('\n['+id+'] '+desc);let rows=d.getCollection(col).aggregate(pipeline).toArray();print('rows='+rows.length);rows.forEach(x=>print(EJSON.stringify(x)));}
print('ORIGINAL BASELINE');printjson({books:d.books.countDocuments({}),readers:d.readers.countDocuments({}),borrow_logs:d.borrow_logs.countDocuments({})});
const a1=[{$group:{_id:'$category',book_count:{$sum:1},avg_rating:{$avg:'$rating'},min_stock:{$min:'$stock'},max_stock:{$max:'$stock'}}},{$sort:{book_count:-1,_id:1}}];
out('A1','分类数及平均评分','books',a1);
out('A2','出版社TOP5，group + topN','books',[{$group:{_id:'$publisher',count:{$sum:1}}},{$group:{_id:null,top_publishers:{$topN:{n:5,sortBy:{count:-1,_id:1},output:{publisher:'$_id',count:'$count'}}}}},{$project:{_id:0,top_publishers:1}}]);
out('A3','各类别图书数量','books',[{$sortByCount:'$category'}]);
out('A4','最高评分三书','books',[{$sort:{rating:-1,isbn:1}},{$limit:3},{$project:{_id:0,title:1,rating:1,borrow_count:1}}]);
out('A5','价格×累计借阅次数（教学计算指标，非真实销售额）','books',[{$project:{_id:0,title:1,estimated_amount:{$round:[{$multiply:['$price','$borrow_count']},2]}}},{$sort:{estimated_amount:-1}}]);
out('A6','按年统计借阅（日期从 $date 导入成 BSON Date）','borrow_logs',[{$group:{_id:{$year:{date:'$borrow_date',timezone:'Asia/Shanghai'}},count:{$sum:1}}},{$project:{_id:0,year:{$concat:[{$toString:'$_id'},'年']},count:1}},{$sort:{year:1}}]);
out('A7','借阅最多读者TOP5','borrow_logs',[{$group:{_id:'$reader_card',borrow_total:{$sum:1}}},{$sort:{borrow_total:-1,_id:1}},{$limit:5}]);
out('A8','联合读者表按学院统计借阅量','readers',[{$lookup:{from:'borrow_logs',localField:'card_no',foreignField:'reader_card',as:'borrows'}},{$project:{college:1,n:{$size:'$borrows'}}},{$group:{_id:'$college',borrow_total:{$sum:'$n'}}},{$sort:{borrow_total:-1,_id:1}}]);
print('\n[A9] merge A1 into category_stats');d.books.aggregate([...a1,{$merge:{into:'category_stats',on:'_id',whenMatched:'replace',whenNotMatched:'insert'}}]).toArray();print('category_stats='+d.category_stats.countDocuments({}));printjson(d.category_stats.find().sort({_id:1}).toArray());
