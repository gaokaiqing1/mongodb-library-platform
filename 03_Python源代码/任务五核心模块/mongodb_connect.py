"""数据库连接配置：Xshell 在 Linux 虚拟机本机运行，密码启动时输入。"""
import getpass
from pymongo import MongoClient
from pymongo.errors import PyMongoError

HOST = '127.0.0.1'
PORT = 27017
DATABASE = 'library'
USERNAME = 'libWriter'
COLLECTIONS = {'books': 'app_books', 'readers': 'app_readers', 'logs': 'app_borrow_logs'}


def connect():
    password = getpass.getpass('请输入 libWriter 数据库密码（输入不回显）：')
    client = MongoClient(host=HOST, port=PORT, username=USERNAME,
                         password=password, authSource=DATABASE,
                         serverSelectionTimeoutMS=5000, tz_aware=True)
    try:
        client.admin.command('ping')
    except PyMongoError:
        client.close()
        raise
    return client, client[DATABASE]


def initialize_work_copies(db):
    """仅首次运行创建业务副本；永不清空已操作过的数据。"""
    mapping = [('books', 'app_books'), ('readers', 'app_readers'),
               ('borrow_logs', 'app_borrow_logs')]
    existing = set(db.list_collection_names())
    for source, target in mapping:
        if target not in existing:
            docs = list(db[source].find({}))
            if docs:
                db[target].insert_many(docs)
            else:
                db.create_collection(target)
            print(f'初始化 {target}: {len(docs)} 条（来源 {source}）')
    print('说明：应用操作只修改 app_ 前缀实验集合，原始数据不变。')


def show_counts(db):
    print('【应用集合文档总数】')
    for name in COLLECTIONS.values():
        print(f'{name}: {db[name].count_documents({})}')
    print('【原始集合文档总数】')
    for name in ('books','readers','borrow_logs'):
        print(f'{name}: {db[name].count_documents({})}')
