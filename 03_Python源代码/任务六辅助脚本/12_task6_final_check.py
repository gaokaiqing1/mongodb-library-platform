# -*- coding: utf-8 -*-
"""Task 6: safe read-only baseline and export-file validation.
Run in CentOS /root/library_project with .venv active.
"""
import getpass
from pathlib import Path
from pymongo import MongoClient

password = getpass.getpass('libWriter password (hidden): ')
client = MongoClient('mongodb://127.0.0.1:27017/', username='libWriter', password=password,
                     authSource='library', serverSelectionTimeoutMS=5000)
try:
    client.admin.command('ping')
    db = client['library']
    counts = {name: db[name].count_documents({}) for name in
              ['books', 'readers', 'borrow_logs', 'category_stats', 'book_in_stock']}
    print('=== TASK 6 BASELINE ===')
    for k, v in counts.items(): print(f'{k}: {v}')
    checks = {
        'Q1 price > 80': db.books.count_documents({'price': {'$gt': 80}}),
        'Q2 stock < 10': db.books.count_documents({'stock': {'$lt': 10}}),
        'Q7 computer rating > 4': db.books.count_documents({'category': '计算机', 'rating': {'$gt': 4}}),
    }
    print('=== QUERY VERIFICATION ===')
    for k, v in checks.items(): print(f'{k}: {v}')
    print('Q14 TOP5:')
    for row in db.books.find({}, {'_id': 0, 'title': 1, 'rating': 1}).sort([('rating',-1),('borrow_count',-1),('_id',1)]).limit(5):
        print(f"  {row.get('title')}: {row.get('rating')}")
    print('A1 category aggregation:')
    pipeline = [{'$group': {'_id': '$category', 'book_count': {'$sum': 1},
                'avg_rating': {'$avg': '$rating'}, 'min_stock': {'$min': '$stock'},
                'max_stock': {'$max': '$stock'}}}, {'$sort': {'book_count': -1, '_id': 1}}]
    agg = list(db.books.aggregate(pipeline))
    for row in agg: print(f"  {row['_id']}: count={row['book_count']}, avg={row['avg_rating']:.4f}")
    expected = {'books':20,'readers':16,'borrow_logs':66,'category_stats':5,'book_in_stock':19}
    expected_queries = {'Q1 price > 80':7,'Q2 stock < 10':8,'Q7 computer rating > 4':7}
    ok = counts == expected and checks == expected_queries and len(agg) == 5
    print('=== FINAL CHECK ===')
    print('PASS' if ok else 'CHECK REQUIRED: compare with reference results')
finally:
    client.close()
