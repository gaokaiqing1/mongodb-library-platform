# -*- coding: utf-8 -*-
"""任务六辅助 JSON 数据备份；Compass 图形化导出仍须单独完成。"""
from pathlib import Path
from getpass import getpass
from pymongo import MongoClient
from bson import json_util
OUT=Path(__file__).resolve().parent/'task6_results'
OUT.mkdir(exist_ok=True)
pw=getpass('请输入 libWriter 数据库密码（不回显）：')
client=MongoClient('127.0.0.1',27017,username='libWriter',password=pw,authSource='library',serverSelectionTimeoutMS=5000)
try:
    client.admin.command('ping')
    db=client.library
    for name in ('books','category_stats'):
        docs=list(db[name].find({}))
        target=OUT/f'{name}_bson_extended_json.json'
        target.write_text(json_util.dumps(docs,ensure_ascii=False,indent=2),encoding='utf-8')
        print(f'EXPORT {name}: {len(docs)} documents -> {target}')
    print('说明：这是脚本辅助备份；ST-6.3还要在Compass中完成导出并截图。')
finally:
    client.close()
    pw=None
