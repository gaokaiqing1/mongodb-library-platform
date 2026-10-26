# -*- coding: utf-8 -*-
"""任务六命令行基线核验：不修改任何数据库文档。"""
from getpass import getpass
from datetime import datetime
from pathlib import Path
import json
from pymongo import MongoClient
from bson import json_util

HOST='127.0.0.1'; PORT=27017
OUT=Path(__file__).resolve().parent/'task6_results'
OUT.mkdir(exist_ok=True)
pw=getpass('请输入 libWriter 数据库密码（不回显）：')
client=MongoClient(HOST, PORT, username='libWriter', password=pw,
                   authSource='library', serverSelectionTimeoutMS=5000)
try:
    client.admin.command('ping')
    d=client['library']
    checks={
        'books':d.books.count_documents({}),
        'readers':d.readers.count_documents({}),
        'borrow_logs':d.borrow_logs.count_documents({}),
        'category_stats':d.category_stats.count_documents({}),
        'Q1_price_gt_80':d.books.count_documents({'price':{'$gt':80}}),
        'Q2_stock_lt_10':d.books.count_documents({'stock':{'$lt':10}}),
        'Q7_computer_rating_gt_4':d.books.count_documents({'category':'计算机','rating':{'$gt':4}}),
        'book_in_stock':d.book_in_stock.count_documents({}),
    }
    print('=== ST-6 BASELINE ===')
    for k,v in checks.items():print(f'{k}: {v}')
    print('=== Q14 TOP FIVE ===')
    top=list(d.books.find({}, {'_id':0,'title':1,'rating':1}).sort([('rating',-1),('borrow_count',-1)]).limit(5))
    for x in top:print(x)
    print('=== A1 CATEGORY SUMMARY ===')
    a1=list(d.books.aggregate([
        {'$group':{'_id':'$category','book_count':{'$sum':1},'avg_rating':{'$avg':'$rating'},'min_stock':{'$min':'$stock'},'max_stock':{'$max':'$stock'}}},
        {'$sort':{'book_count':-1,'_id':1}}
    ]))
    for x in a1:print(x)
    print('=== COLLECTION TYPES ===')
    types=[]
    for x in d.list_collections():
        if x['name'] in ['books','readers','borrow_logs','category_stats','book_logs','book_in_stock']:
            t={'name':x['name'],'type':x.get('type'), 'options':x.get('options',{})}
            types.append(t)
            print(x['name'],x.get('type'),x.get('options',{}))
    result={'checks':checks,'Q14':top,'A1':a1,'collection_types':types,'captured_at':datetime.now().isoformat()}
    (OUT/'task6_baseline.json').write_text(json_util.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    expected={'books':20,'readers':16,'borrow_logs':66,'category_stats':5,'Q1_price_gt_80':7,'Q2_stock_lt_10':8,'Q7_computer_rating_gt_4':7,'book_in_stock':19}
    mismatches={k:(checks[k],v) for k,v in expected.items() if checks[k]!=v}
    print('=== BASELINE CHECK ===')
    if mismatches:print('ATTENTION: baseline differs (actual,expected):',mismatches)
    else:print('PASS: expected original baseline values all match')
    print('Saved:',OUT/'task6_baseline.json')
finally:
    client.close()
    pw=None
