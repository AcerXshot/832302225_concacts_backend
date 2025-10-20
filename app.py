import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# --- 辅助函数：获取数据库连接 ---
# 这个函数能让我们用像字典一样的方式访问数据库的行，更方便
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # 这一行是关键！
    return conn



# 【查】GET /api/contacts - 获取所有联系人
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    conn = get_db_connection()
    # 执行 SQL 查询
    contacts_rows = conn.execute('SELECT * FROM contacts').fetchall()
    conn.close()
    # 将查询结果（Row对象列表）转换为字典列表，以便 jsonify
    contacts = [dict(row) for row in contacts_rows]
    return jsonify(contacts)


# 【增】POST /api/contacts - 添加一个新联系人
@app.route('/api/contacts', methods=['POST'])
def add_contact():
    new_contact = request.get_json()
    name = new_contact['name']
    phone = new_contact['phone']

    conn = get_db_connection()
    cursor = conn.cursor()
    # 使用 ? 作为占位符可以防止 SQL 注入攻击，非常安全
    cursor.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))

    new_id = cursor.lastrowid  # 获取刚刚插入的数据的 ID

    conn.commit()  # 提交更改
    conn.close()

    # 返回新创建的联系人信息
    return jsonify({'id': new_id, 'name': name, 'phone': phone}), 201


# 【改】PUT /api/contacts/<id> - 修改一个联系人
@app.route('/api/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact_updates = request.get_json()
    name = contact_updates['name']
    phone = contact_updates['phone']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE contacts SET name = ?, phone = ? WHERE id = ?', (name, phone, id))

    conn.commit()
    conn.close()

    # 检查是否有行被更新
    if cursor.rowcount == 0:
        return jsonify({'error': '联系人未找到'}), 404
    else:
        return jsonify({'id': id, 'name': name, 'phone': phone})


# 【删】DELETE /api/contacts/<id> - 删除一个联系人
@app.route('/api/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = ?', (id,))

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': '联系人未找到'}), 404
    else:
        return jsonify({'message': '删除成功'})


# ----------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)