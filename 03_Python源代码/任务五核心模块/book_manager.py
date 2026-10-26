"""图书增删改查、条件检索及评分排行。"""
from datetime import datetime, timezone
from pymongo.errors import DuplicateKeyError

C = 'app_books'

def show(books):
    for b in books:
        print(f"ISBN={b.get('isbn')} | {b.get('title')} | 分类={b.get('category')} | "
              f"定价={b.get('price')} | 库存={b.get('stock')} | 评分={b.get('rating')}")

def search(db):
    keyword = input('书名或作者关键字（直接回车查前10本）：').strip()
    query = {'$or': [{'title': {'$regex': keyword, '$options': 'i'}},
                     {'author': {'$regex': keyword, '$options': 'i'}}]} if keyword else {}
    docs = list(db[C].find(query).sort('title',1).limit(10))
    if not docs: print('查询无结果')
    else: show(docs)
    print(f'本页展示 {len(docs)} 条；全部匹配 {db[C].count_documents(query)} 条')

def exact(db):
    isbn = input('输入 ISBN：').strip()
    b = db[C].find_one({'isbn': isbn})
    if b: show([b])
    else: print('查询无结果')

def filtered(db):
    category = input('类别（留空不限制）：').strip()
    try:
        low = float(input('最低价格（留空按0）：').strip() or '0')
        high = float(input('最高价格（留空按999999）：').strip() or '999999')
    except ValueError:
        print('价格应为数字'); return
    q = {'price': {'$gte': low, '$lte': high}}
    if category: q['category'] = category
    docs = list(db[C].find(q).sort('price',1).limit(20))
    if docs: show(docs)
    else: print('查询无结果')
    print('匹配条数:',db[C].count_documents(q))

def ranking(db):
    docs = list(db[C].find().sort([('rating',-1),('borrow_count',-1)]).limit(5))
    if docs: show(docs)
    else: print('查询无结果')

def add(db):
    isbn=input('新书 ISBN：').strip(); title=input('书名：').strip()
    if not isbn or not title: print('ISBN 和书名不能为空');return
    if db[C].find_one({'isbn':isbn}): print('ISBN 已存在，不重复插入'); return
    try:
        price=float(input('价格：')); stock=int(input('库存：'))
        rating=float(input('评分0-5（默认0）：') or '0')
        if price<0 or stock<0 or not 0<=rating<=5: raise ValueError()
    except ValueError:
        print('价格、库存或评分不合法');return
    doc={'isbn':isbn,'title':title,'author':input('作者：'),
         'publisher':input('出版社：'),'category':input('类别：'),
         'price':price,'stock':stock,'rating':rating,'tags':[],
         'publish_date':datetime.now(timezone.utc),'borrow_count':0}
    try:
        result=db[C].insert_one(doc)
        print('insert_one成功，插入数=1，ID=',result.inserted_id)
    except DuplicateKeyError: print('ISBN 唯一约束阻止重复添加')

def add_many_demo(db):
    """insert_many 方法演示，仅在明确确认后插入。"""
    if input('插入两本演示图书? 输入 YES 确认：')!='YES': return
    docs=[]
    for k in (1,2):
        isbn='APP-DEMO-BOOK-'+str(k)
        if db[C].find_one({'isbn':isbn}): continue
        docs.append({'isbn':isbn,'title':f'应用演示图书{k}','author':'实验',
                     'publisher':'实验出版社','category':'实验类','price':10.0,
                     'stock':3,'rating':4.0,'tags':['演示'],'borrow_count':0})
    if docs:
        r=db[C].insert_many(docs); print('insert_many插入数=',len(r.inserted_ids))
    else: print('演示图书已存在，本次插入0条')

def change_stock(db):
    isbn=input('待修改库存的 ISBN：').strip()
    try: delta=int(input('库存增减量（负数表示减少）：'))
    except ValueError: print('请输入整数');return
    b=db[C].find_one({'isbn':isbn})
    if not b: print('查询无结果');return
    if b.get('stock',0)+delta<0:print('库存不能为负数');return
    r=db[C].update_one({'isbn':isbn},{'$inc':{'stock':delta}})
    print(f'匹配数={r.matched_count}，修改数={r.modified_count}')

def remove(db):
    isbn=input('待删除图书 ISBN：').strip()
    b=db[C].find_one({'isbn':isbn})
    if not b: print('查询无结果');return
    print('将删除：',b.get('title'))
    if input('输入 DELETE 确认：')!='DELETE': print('已取消');return
    r=db[C].delete_one({'isbn':isbn});print('delete_one删除数=',r.deleted_count)

def remove_demos(db):
    if input('清除所有APP-DEMO-BOOK示例? 输入 DELETE 确认：')!='DELETE':return
    r=db[C].delete_many({'isbn':{'$regex':'^APP-DEMO-BOOK-'}})
    print('delete_many删除数=',r.deleted_count)
