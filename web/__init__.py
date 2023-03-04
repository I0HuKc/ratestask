from flask import Flask, jsonify

from database import db_conn

app = Flask(__name__)

@app.route("/")
def index():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM ports;')
    ports = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(ports)