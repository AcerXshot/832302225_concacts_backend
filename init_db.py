import sqlite3

# 连接到数据库文件（如果文件不存在，则会自动创建）
connection = sqlite3.connect('phone.db')

# 创建一个 Cursor 对象，用来执行 SQL 语句
cursor = connection.cursor()

# IF NOT EXISTS 确保了如果我们重复运行这个脚本，它不会因为表已存在而报错
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL
);
""")
# ----------------------------------------

#cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", ('Clark Kent', '123456789'))
#cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", ('Bruce Wayne', '987654321'))

# 提交事务（保存更改）
connection.commit()

# 关闭数据库连接
connection.close()

print("数据库 'phone.db' 已成功初始化。")