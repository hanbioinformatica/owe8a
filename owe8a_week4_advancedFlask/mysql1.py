# https://www.youtube.com/watch?v=ShsaaKsd_28
# http://more-codes.com/2018/09/17/building-a-todo-list-with-flask-reactjs-and-mysql/


# created table: create table tasks (id int primary key auto_increment, title text);

from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)

app.config['MYSQL_USER'] = 'dummy@hannl-hlo-bioinformatica-mysqlsrv'
app.config['MYSQL_PASSWORD'] = 'blaat1234'
app.config['MYSQL_DB'] = 'dummy'
app.config['MYSQL_HOST']='hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
CORS(app)

@app.route('/api/tasks', methods=['GET'])
def get_all_tasks():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    rv = cur.fetchall()
    print('done select')
    return jsonify(rv)

@app.route('/api/task', methods=['POST'])
def add_task():
    cur = mysql.connection.cursor()
    title = request.get_json()['title']

    cur.execute("INSERT INTO tasks (title) VALUES ('" + str(title) + "')")
    mysql.connection.commit()
    result = {'title':title}

    return jsonify({"result": result})

@app.route("/api/task/<id>", methods=['PUT'])
def update_task(id):
    cur = mysql.connection.cursor()
    title = request.get_json()['title']
    
    cur.execute("UPDATE tasks SET title = '" + str(title) + "' where id = " + id)
    mysql.connection.commit()

    result = {"title": title}

    return jsonify({"result": result})

@app.route("/api/task/<id>", methods=['DELETE'])
def delete_task(id):
    cur = mysql.connection.cursor()
    response = cur.execute("DELETE FROM tasks where id = " + id)
    mysql.connection.commit()

    if response > 0:
        result = {'message' : 'record deleted'}
    else:
        result = {'message' : 'no record found'}
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)