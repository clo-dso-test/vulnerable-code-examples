from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 1. 동적 SQL 문자열 연결 (취약한 방식)
def get_user_data(user_id):
    conn = get_db_connection()
    query = "SELECT * FROM users WHERE id = " + user_id  # SQL Injection 가능
    result = conn.execute(query).fetchall()
    conn.close()
    return result

# 2. 외부 입력을 그대로 SQL에 삽입 (취약한 방식)
@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get("q")
    conn = get_db_connection()
    query = f"SELECT * FROM products WHERE name LIKE '%{keyword}%'"  # SQL Injection 가능
    result = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(row) for row in result])

# 3. 사용자 입력 기반 관리자 계정 인증 우회 (취약한 방식)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    conn = get_db_connection()
    query = "SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username, password)  # SQL Injection 가능
    result = conn.execute(query).fetchone()
    conn.close()
    return jsonify({"success": result is not None})

if __name__ == '__main__':
    app.run(debug=True)
