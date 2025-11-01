import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# --- 数据库初始化 ---
def init_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # 为 contacts 表添加一个新的 email 字段，允许为空
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS contacts
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       name
                       TEXT
                       NOT
                       NULL,
                       phone
                       TEXT
                       NOT
                       NULL,
                       email
                       TEXT
                   );
                   """)

    # --- 升级表结构 ---
    # 这是一个安全的操作，尝试添加 email 列，如果它已存在则什么也不做
    try:
        cursor.execute("ALTER TABLE contacts ADD COLUMN email TEXT")
    except sqlite3.OperationalError:
        # 'duplicate column name: email' 错误是正常的，说明列已存在
        pass

    conn.commit()
    conn.close()


# ---------------------------------------------

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# --- API 接口 (已全部更新) ---

@app.route('/')
def index():
    return "Backend server is running. Access the API at /api/contacts"


# 【查】GET /api/contacts (已更新)
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    query = request.args.get('q', '')
    conn = get_db_connection()
    if query:
        search_term = f"%{query}%"
        # 搜索也支持 email
        contacts_rows = conn.execute(
            'SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?',
            (search_term, search_term, search_term)
        ).fetchall()
    else:
        contacts_rows = conn.execute('SELECT * FROM contacts').fetchall()
    conn.close()
    contacts = [dict(row) for row in contacts_rows]
    return jsonify(contacts)


# 【增】POST /api/contacts (已更新)
@app.route('/api/contacts', methods=['POST'])
def add_contact():
    new_contact = request.get_json()
    name = new_contact['name']
    phone = new_contact['phone']
    # 接收 email，如果不存在则为 None
    email = new_contact.get('email')

    print(f"!!! 接收到的数据: {new_contact}, 提取的 Email: {email}")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({'id': new_id, 'name': name, 'phone': phone, 'email': email}), 201


# 【改】PUT /api/contacts/<id> (已更新)
@app.route('/api/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact_updates = request.get_json()
    name = contact_updates['name']
    phone = contact_updates['phone']
    email = contact_updates.get('email')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?', (name, phone, email, id))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': '联系人未找到'}), 404
    else:
        return jsonify({'id': id, 'name': name, 'phone': phone, 'email': email})


# 【删】DELETE /api/contacts/<id> (保持不变)
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


# --- 主程序入口 ---
if __name__ == '__main__':
    init_database()
    app.run(debug=True)

with app.app_context():
    init_database()

