"""读者查询、学院统计、等级分布。"""
C='app_readers'

def search(db):
    s=input('姓名或借阅证号：').strip()
    q={'$or':[{'name':{'$regex':s}},{'card_no':{'$regex':s}}]} if s else {}
    rows=list(db[C].find(q).limit(20))
    if not rows:print('查询无结果');return
    for x in rows:
        print(x.get('card_no'),x.get('name'),x.get('college'),x.get('level'))
    print('匹配数量=',db[C].count_documents(q))

def college(db):
    names=sorted(x for x in db[C].distinct('college') if x)
    if not names: print('查询无结果');return
    for n in names:
        print(f'{n}: {db[C].count_documents({"college":n})}人')

def levels(db):
    values=sorted(x for x in db[C].distinct('level') if x)
    if not values:print('查询无结果');return
    for level in values:
        print(f'{level}: {db[C].count_documents({"level":level})}人')
