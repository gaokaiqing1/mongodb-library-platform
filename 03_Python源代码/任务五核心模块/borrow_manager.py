"""借阅登记和归还演示：在普通 app_borrow_logs 副本中操作。"""
from datetime import datetime,timezone

C='app_borrow_logs'

def register(db):
    card=input('借阅证号：').strip();isbn=input('图书ISBN：').strip()
    if not db['app_readers'].find_one({'card_no':card}):print('该读者不存在');return
    book=db['app_books'].find_one({'isbn':isbn})
    if not book:print('该图书不存在');return
    if book.get('stock',0)<1:print('库存不足');return
    now=datetime.now(timezone.utc)
    doc={'reader_card':card,'book_isbn':isbn,'borrow_date':now,'status':'借出'}
    # 避免破坏真实历史流水；两处修改用于课程演示，不保证跨集合事务原子性。
    r=db[C].insert_one(doc)
    updated=db['app_books'].update_one({'isbn':isbn,'stock':{'$gte':1}},
                      {'$inc':{'stock':-1,'borrow_count':1}})
    if updated.modified_count!=1:
        db[C].delete_one({'_id':r.inserted_id})
        print('库存同时发生变化，已取消本次登记');return
    print('借阅登记插入数=1，库存修改数=',updated.modified_count,'记录ID=',r.inserted_id)

def return_book(db):
    card=input('借阅证号：').strip();isbn=input('图书ISBN：').strip()
    q={'reader_card':card,'book_isbn':isbn,'status':'借出'}
    rows=list(db[C].find(q).sort('borrow_date',-1).limit(1))
    if not rows:print('未查询到未归还的借阅记录');return
    r=db[C].update_many({'_id':rows[0]['_id'],'status':'借出'},
                          {'$set':{'status':'已归还','return_date':datetime.now(timezone.utc)}})
    if r.modified_count:
        stock=db['app_books'].update_one({'isbn':isbn},{'$inc':{'stock':1}})
        print('归还记录更新数=',r.modified_count,'库存更新数=',stock.modified_count)
    else: print('归还记录更新数=0')

def overdue(db):
    # 教学数据状态逾期并不意味着没有归还日期；明确采用「逾期且未归还」。
    q={'status':'逾期','return_date':{'$exists':False}}
    rows=list(db[C].find(q).limit(20))
    print('逾期且未归还：',db[C].count_documents(q),'条')
    if not rows:print('查询无结果')
    for x in rows:print(x.get('reader_card'),x.get('book_isbn'),x.get('borrow_date'))
