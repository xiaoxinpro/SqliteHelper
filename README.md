## SqliteHelper for Python

## 简介
SqliteHelper是一个基于Python和Sqlite3的助手类库，根据实际使用大大简化数据库增删改查的操作，助手类库采用连贯操作，使开发更加灵活速度进一步得到提高。

## 开始使用
只需将 `SqliteHelper.py` 文件复制到项目目录下，在需要操作数据库的代码中添加以下引用：
```
import SqliteHelper
```

## 连接数据库
连接数据库只需要提供数据库路径即可，使用下面的代码，连接到数据库文件并返回一个数据库对象。
```
testDb = SqliteHelper.Connect(r'数据库路径')
```

> 如果数据库路径存在则直接连接数据库，若数据库不存在则在该路径下自动创建一个数据库文件并连接。

有些项目不需要保存数据库文件，则可以使用下面的代码直接将数据库创建到内存中。
```
testDb = SqliteHelper.Connect()
```

> 需要注意，在内存中创建的数据具有更快的读写速度，但释放掉内存的同时数据库将永久丢失。

## 连贯操作
连贯操作也有称作链式操作的，本助手类库全部方法均基于连贯操作来实现的，所有连贯操作的起点均来自 `数据库对象` ，即连接数据库示例代码中的 `testDb` 变量。

连贯操作的使用十分简单，假如我们要查询用户数据表中id小于100的前5个用户名，按照id值降序排列，代码如下：
```
ret = testDb.table('user').where('id < 100').order('id desc').field('username').find(5)
```
以上示例中`table`为数据表指定的方法必须放在开头；`where`、`order`、`field`方法就是连贯操作方法，连贯操作方法的顺序可以随意，不按照示例中的顺序摆放也是可以的；而`find`是实际操作的方法，必须放在最后。

系统中支持的连贯操作方法如下表：

连贯操作方法 | 作用 | 支持的参数类型
:-: | :-: | :-:
where | 用于查询或者更新条件的定义 | str、dict
data | 用于新增数据之前的数据对象赋值 | list、tuple、dict
field | 用于定义查询要输出的字段 | str、list、tuple
order | 用于对结果排序 | str、list、dict

具体连贯操作方法的使用在后续章节中将详细介绍说明。


## 创建表
创建表之前需要成功连接到数据库，然后使用`table`函数指定表名，最后调用`create`方法完成创建，示例代码如下：
```
testDb.table('user').create({
    'id': 'INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
    'username': 'TEXT NOT NULL',
    'password': 'TEXT NOT NULL'
})
```

以上创建方法 `create` 只用到一个参数，参数建议使用dict的格式，key为字段名称，value为该字段的数据格式。

另外也可以使用str或list作为参数，示例代码如下：

```
# 使用str参数创建表
testDb.table('user').create('id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL')

# 使用list参数创建表
testDb.table('user').create([
    'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
    'username TEXT NOT NULL',
    'password TEXT NOT NULL'
])
```

具体使用哪种创建方法可按照自己的习惯来选择是使用，以上三种方法效果是相同的。

> 需要注意的是，只有数据表不存在的时候才会进行创建，若检测到表名已存在则直接跳过。因此在执行创建方法前可以不用检查表名是否存在。

### 创建表并添加数据
有些使用场景是在创建完成数据表后添加一些初始化的数据，这就使用到`create`的第二参数`insert`，实例代码如下：
```
testDb.table('user').create({
    'id': 'INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
    'username': 'TEXT NOT NULL',
    'password': 'TEXT NOT NULL'
}, insert=[
    {'username': 'demo', 'password': 'xxgzs.org'},
    {'username': 'admin', 'password': 'admin888'},
    {'username': 'test', 'password': 'test123'}
])
```
这里的`insert`参数和连贯操作方法中的`data`方法参数时相同的，详细可参阅添加数据章节，这里不再过多赘述。

> 若数据已存在，则不会执行创建数据表的操作，同时也不会添加`insert`参数中的数据。

### 返回值
`create`方法是有返回值的，创建成功是返回True，创建失败时返回False或报告异常，如果不需要使用可以直接忽略掉。

## 添加数据
数据添加的方法使用`add`方法，使用示例如下：
```
testDb.table('user').add({
    'username': 'test1', 
    'password': 'test_pw_1'
})
```

对于增加单条数据，建议直接使用`add`方法。

`add`方法的参数是一个`dict`格式的变量，key为字段名称，value是要添加的值（可以是int、float、str格式的变量）。

> 需要注意的是，字段名必须已存在的，否则将报异常。

### 使用连贯操作方法data
对于添加多条数据来说，使用`add`方法效率十分低下，建议使用`data`连贯操作方法来实现，示例代码如下：
```
testDb.table('user').data([
    {'username': 'test3', 'password': 'test_pw_3'},
    {'username': 'test4', 'password': 'test_pw_4'},
    {'username': 'test5', 'password': 'test_pw_5'},
]).add()
```

`data`方法的参数是多个`dict`格式变量组成的`list`，其中`dict`变量与`add`方法中的参数相同。

> `add`方法前使用了连贯操作后必须不能带有任何参数，否则将覆盖掉连贯操作方法。

### 返回值
此方法无返回值

## 查询数据
数据查询的方式有很多中，而且还包括多种连贯操作，为了方便说明，首先介绍连贯操作方法。

### 查询连贯操作方法 where
在所有的连贯操作方法中，where方法使用的频率是最高的，功能也是最多的。

#### 字符串条件
使用字符串条件直接查询数据，示例代码如下：
```
testDb.table('user').where("id = 1 AND username = 'demo'")
```
字符串条件可以理解为使用SQL语句条件进行查询，上例中对应的SQL代码如下：
```
SELECT * FROM user WHERE id = 1 AND username = 'demo'
```
不难发现，`where`方法中的参数与SQL语句中`WHERE`参数完全相同。

#### 字典条件
顾名思义，即是使用`dict`作为`where`方法的参数，示例代码如下：
```
ret = testDb.table('user').where({
    'id' : ['>', 0],
    'username': 'demo',
    'password': 'xxgzs.org'
}).find()
```

`where`方法的参数`dict`的key为查询的字段名（必须是表中已存在的字段，若不存在则直接报错），value分为两种情况：
- value为str、int、float时则进行` = `匹配
- value为list是则以list[0]作为表达式，list[1]作为查询条件进行匹配

可以理解为：
```
dict['字段名0'] = '查询条件0'
dict['字段名1'] = list['表达式1','查询条件1']
dict['字段名2'] = list['表达式2','查询条件2']
数据库对象.table('表名').where(dict).find()
```

字典条件中支持的表达式如下：

 表达式 | 含义 
 :-: | :-: 
 = | 等于
 <> | 不等于
 > | 大于
 >= | 大于等于
 < | 小于
 <= | 小于等于
 LIKE | 模糊查询

另外在字典条件中，`where`存在另一个可选参数`condition`,可以用来指定多个表达式之间的关系，默认是`and`,如需要或条件可设置成`or`

### 字段连贯操作方法 field
`field`方法用于查询结果输出的指定字段名称，如果不包含该方法则输出全部字段。

```
testDb.table('user').field('username','password').where('id = 1').find()
```

如上示例，输出结果中将只包含'username'和'password'字段。

> 需要注意的是`field`参数必须是存在的字段名，否则将抛异常。


### 排序连贯操作方法 order
`order`方法用于查询结果排序，示例代码如下：
```
table('user').order('username').findAll()
```

`order`参数默认只需要填写字段名，默认是进行指定字段升序排序。

若需要进行降序排序可将参数改为`'username desc'`,即可。

另外也可以进行多字段排序，优先级从左到右依次进行，字段间使用`,`分隔，例如以下代码：

```
ret = testDb.table('user').order('id asc, username desc').findAll()
```


## 更新数据
数据更新的方法使用`save`方法，示例代码如下：
```
testDb.table('user').where('id = 1').save({'password': '1234567'})
```

`save`方法的参数是一个`dict`格式的变量，其key为要更新的字段名称，value是要更新的值（可以是int、float、str格式的变量）。

> 建议`save`方法配合`where`连贯操作执行，否则将更新表中全部数据。

`where`连贯操作方法的使用请参照查找数据章节，这里不再赘述。

## 删除数据
数据删除的方法使用`delete`方法，示例代码如下：
```
testDb.table('user').where('id >= 2 and id < 5').delete()
```

`delete`方法没有参数。

> 建议`delete`方法配合`where`连贯操作执行，否则将删除表中全部数据。

`where`连贯操作方法的使用请参照查找数据章节，这里不再赘述。
