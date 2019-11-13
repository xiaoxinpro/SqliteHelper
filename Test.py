#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import SqliteHelper

# 声明测试数据库路径
DB_FILE_PATH = r'./SqliteHelper/test.db'
if os.path.exists(DB_FILE_PATH):
    # 删除之前的测试文件
    os.remove(DB_FILE_PATH)

# 连接数据库文件（没有则创建）
testDb = SqliteHelper.Connect(DB_FILE_PATH)

# 创建表（存在则跳过）
# testDb.table('user').create({
#     'id': 'INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
#     'username': 'TEXT NOT NULL',
#     'password': 'TEXT NOT NULL'
# })

# 创建表并添加数据
testDb.table('user').create({
    'id': 'INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
    'username': 'TEXT NOT NULL',
    'password': 'TEXT NOT NULL'
}, insert=[
    {'username': 'demo', 'password': 'xxgzs.org'},
    {'username': 'admin', 'password': 'admin888'},
    {'username': 'test', 'password': 'test123'}
])

# 插入数据
testDb.table('user').add({'username': 'test1', 'password': 'test_pw_1'})
testDb.table('user').data({'username': 'test2', 'password': 'test_pw_2'}).add()
testDb.table('user').data([
    {'username': 'test3', 'password': 'test_pw_3'},
    {'username': 'test4', 'password': 'test_pw_4'},
    {'username': 'test5', 'password': 'test_pw_5'},
]).add()

# 插入不存在字段数据将自动过滤掉
testDb.table('user').add({'username': 'xiaoxin', 'password': 'xxgzs.org', 'test': 'null...'})

# 查找全部数据
ret = testDb.table('user').findAll()
print('查找全部数据:', ret)

# 查找指定条件的数据
ret = testDb.table('user').where("id >= 1 and username = 'demo' and password = 'xxgzs.org'").find()
ret = testDb.table('user').where({
    'id' : ['>=', 1],
    'username': 'demo',
    'password': 'xxgzs.org',
}).find()
ret = testDb.table('user').where({
    'id' : ['>=', 1],
    'username': 'demo',
    'password': 'xxgzs.org'
}, 'and').find()
ret = testDb.table('user').where({
    'id' : ['>=', 1],
    'username': 'demo',
    'password': 'xxgzs.org'
}, ['and','and']).find()
ret = testDb.table('user').where({
    'id' : ['>=', 1],
    'username': 'demo',
    'password': 'xxgzs.org',
    'test': 'null++'
}).find()
print('查找指定条件的数据:', ret)

# 查询并排序数据
# ret = testDb.table('user').order('username').findAll()
# ret = testDb.table('user').order('username asc').findAll()
ret = testDb.table('user').order({'username': 'asc'}).findAll()
print('查询并排序数据:', ret)

# 查询并倒序排序
ret = testDb.table('user').order('username desc').findAll()
ret = testDb.table('user').order({'username': 'desc'}).findAll()
print('查询并倒序排序:', ret)

# 查询结果返回指定数量
ret = testDb.table('user').find(3)
print('查询结果返回指定数量:', ret)

# 查询结果分页返回(页面从0开始计数)
ret = testDb.table('user').find(3, page=0)
print('查询结果分页返回1:', ret)
ret = testDb.table('user').find(3, page=1)
print('查询结果分页返回2:', ret)
ret = testDb.table('user').find(3, page=2)
print('查询结果分页返回3:', ret)

# 查询结果返回指定列
ret = testDb.table('user').field('username','password').where('id = 1').find()
ret = testDb.table('user').field('username','password','test').where('id = 1').find()
print('查询结果返回指定列:', ret)

# 更新数据(忽略where将改变全部数据)
testDb.table('user').where('id = 1').save({'password': '1234567'})
ret = testDb.table('user').where('id = 1').find()
print('更新数据结果:', ret)

# 删除数据(忽略where将删除全部数据)
testDb.table('user').where('id >= 2 and id < 5').delete()
ret = testDb.table('user').findAll()
print('删除数据结果:', ret)

# 统计查询 Count
ret = testDb.table('user').count()
ret = testDb.table('user').count('id')
print('统计查询Count:', ret)

# 统计查询 Max
ret = testDb.table('user').max('id')
print('统计查询Max:', ret)

# 统计查询 Min
ret = testDb.table('user').min('id')
print('统计查询Min:', ret)

# 统计查询 Avg
ret = testDb.table('user').avg('id')
print('统计查询Avg:', ret)

# 统计查询 Sum
ret = testDb.table('user').sum('id')
print('统计查询Sum:', ret)

# 模糊查询
ret = testDb.table('user').where({'username': ['like', '%test%']}).findAll()
print('模糊查询test:', ret)

# 执行纯SQL命令，返回sqlite类中的cursor结构
ret = testDb.query("SELECT * FROM user")
print('执行纯SQL命令:', ret.fetchall())

# 关闭数据库连接
testDb.close()
