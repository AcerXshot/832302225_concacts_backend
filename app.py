import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- 将初始化数据库的逻辑封装成一个函数 ---
def init_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # 只有当 contacts 表不存在时，才创建它
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()
# ---------------------------------------------

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- API 接口  ---
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    conn = get_db_connection()
    contacts_rows = conn.execute('SELECT * FROM contacts').fetchall()
    conn.close()
    contacts = [dict(row) for row in contacts_rows]
    return jsonify(contacts)


@app.route('/api/contacts', methods=['POST'])
def add_contact():
    new_contact = request.get_json()
    name = new_contact['name']
    phone = new_contact['phone']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'id': new_id, 'name': name, 'phone': phone}), 201

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
    if cursor.rowcount == 0:
        return jsonify({'error': '联系人未找到'}), 404
    else:
        return jsonify({'id': id, 'name': name, 'phone': phone})

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



if __name__ == '__main__':
    init_database() # 在本地运行前，也确保数据库已初始化
    app.run(debug=True)

# --- 为 Render 部署环境确保数据库初始化 ---
# 当 Gunicorn 启动应用时，它会导入这个文件，这段代码就会被执行
with app.app_context():
    init_database()
