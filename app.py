from flask import Flask, jsonify, request
from flask_cors import CORS
import time # 用来生成简单的唯一ID

app = Flask(__name__)
CORS(app) # 允许跨域

# --- 模拟数据库 ---
# 用一个列表来存储所有的联系人数据
# 每个联系人是一部字典(dictionary)
contacts_db = [
    {"id": 1, "name": "张三", "phone": "13800138000"},
    {"id": 2, "name": "李四", "phone": "13900139000"}
]
# 用于生成新的联系人ID
next_id = 3
# --------------------


@app.route('/')
def hello_world():
    return '后端服务器已启动!'

# GET /api/contacts - 获取所有联系人
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    return jsonify(contacts_db)


@app.route('/api/contacts', methods=['POST'])
def add_contact():
    global next_id  # 声明我们要修改全局变量 next_id

    # 从前端发送的JSON请求体中获取数据
    new_contact_data = request.get_json()

    # 创建新的联系人对象
    contact = {
        "id": next_id,
        "name": new_contact_data['name'],
        "phone": new_contact_data['phone']
    }

    # "存入数据库"
    contacts_db.append(contact)
    next_id += 1

    # 返回成功信息和新创建的联系人
    return jsonify(contact), 201


@app.route('/api/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    # 在数据库(列表)中查找具有相应id的联系人
    contact_to_delete = None
    for contact in contacts_db:
        if contact['id'] == id:
            contact_to_delete = contact
            break

    if contact_to_delete:
        contacts_db.remove(contact_to_delete)
        return jsonify({"message": "删除成功"}), 200
    else:
        return jsonify({"error": "联系人未找到"}), 404  # 404 Not Found


@app.route('/api/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    # 从前端发送的JSON请求体中获取更新后的数据
    updated_data = request.get_json()

    # 在数据库(列表)中查找具有相应id的联系人
    contact_to_update = None
    for contact in contacts_db:
        if contact['id'] == id:
            contact_to_update = contact
            break

    if contact_to_update:
        # 更新联系人的姓名和电话
        contact_to_update['name'] = updated_data.get('name', contact_to_update['name'])
        contact_to_update['phone'] = updated_data.get('phone', contact_to_update['phone'])
        return jsonify(contact_to_update), 200 # 200 OK
    else:
        return jsonify({"error": "联系人未找到"}), 404 # 404 Not Found


if __name__ == '__main__':
    app.run(debug=True)