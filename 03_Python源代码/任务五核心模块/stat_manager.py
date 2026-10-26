"""三个必做的 PyMongo 聚合管道。"""

def category_stats(db):
    pipeline=[{'$group':{'_id':'$category','total_stock':{'$sum':'$stock'},
                           'avg_price':{'$avg':'$price'},'book_count':{'$sum':1}}},
              {'$sort':{'total_stock':-1,'_id':1}}]
    rows=list(db['app_books'].aggregate(pipeline))
    if not rows:print('查询无结果')
    for r in rows:
        print(f"{r['_id']} | 库存合计={r['total_stock']} | 平均价格={r['avg_price']:.2f} | 图书数={r['book_count']}")

def year_trend(db):
    pipeline=[{'$group':{'_id':{'$year':'$borrow_date'},'total':{'$sum':1}}},
              {'$sort':{'_id':1}},
              {'$project':{'_id':0,'year':{'$concat':[{'$toString':'$_id'},'年']},'total':1}}]
    rows=list(db['app_borrow_logs'].aggregate(pipeline))
    if not rows:print('查询无结果')
    for r in rows:print(r['year'],r['total'],'条')

def popularity(db):
    pipeline=[{'$sort':{'borrow_count':-1,'title':1}},
              {'$limit':5},{'$project':{'_id':0,'title':1,'borrow_count':1}}]
    rows=list(db['app_books'].aggregate(pipeline))
    if not rows:print('查询无结果')
    for i,r in enumerate(rows,1): print(i,r.get('title'),r.get('borrow_count',0),'次')
