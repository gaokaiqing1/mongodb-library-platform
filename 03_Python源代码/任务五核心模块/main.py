"""任务五菜单主程序；默认所有变更只作用于 app_ 实验副本。"""
from pymongo.errors import PyMongoError
from mongodb_connect import connect,initialize_work_copies,show_counts
import book_manager as books
import reader_manager as readers
import borrow_manager as borrow
import stat_manager as stats

OPTIONS={
 '1':('图书关键字检索',books.search),
 '2':('ISBN精确查找',books.exact),
 '3':('类别和价格范围查询',books.filtered),
 '4':('图书评分前五名',books.ranking),
 '5':('添加单本图书 insert_one',books.add),
 '6':('批量添加演示图书 insert_many',books.add_many_demo),
 '7':('更改库存 update_one',books.change_stock),
 '8':('删除单本图书 delete_one',books.remove),
 '9':('批量清理演示图书 delete_many',books.remove_demos),
 '10':('读者查询',readers.search),
 '11':('各学院读者数量',readers.college),
 '12':('读者等级分布',readers.levels),
 '13':('借阅登记 insert_one',borrow.register),
 '14':('图书归还 update_many',borrow.return_book),
 '15':('逾期未还记录查询',borrow.overdue),
 '16':('分类库存、均价、图书数聚合',stats.category_stats),
 '17':('年度借阅趋势聚合',stats.year_trend),
 '18':('热门图书前五名聚合',stats.popularity),
 '19':('查看文档总数',show_counts),
}

def main():
    client=None
    try:
        client,db=connect()
        print('\n[连接成功] MongoDB library，用户 libWriter')
        initialize_work_copies(db)
        show_counts(db)
        while True:
            print('\n========== 图书情报检索与统计平台 =========')
            for k,(name,_) in OPTIONS.items(): print(f'{k:>2}. {name}')
            print(' 0. 退出程序')
            action=input('请选择功能编号：').strip()
            if action=='0': print('程序退出，正在关闭数据库连接');break
            item=OPTIONS.get(action)
            if not item:print('菜单编号无效，请重新输入');continue
            try: item[1](db)
            except (PyMongoError,ValueError) as exc:
                print('操作失败：',type(exc).__name__,str(exc)[:240])
    except PyMongoError as exc:
        print('数据库连接失败：',type(exc).__name__,str(exc)[:300])
        print('请检查 mongod 是否运行、libWriter 密码和本地 27017 端口。')
    finally:
        if client is not None:
            client.close()
            print('MongoClient 已关闭')

if __name__=='__main__':main()
