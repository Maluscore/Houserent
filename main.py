from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from utils import log, total_digit

import sqlite3

app = Flask(__name__)
app.secret_key = 'random'


@app.route('/')
def index_view():
    return render_template('index.html')


@app.route('/gongyu', methods=['POST'])
def data_post():
    form = request.get_json()
    min_val = form.get('minVal', '')
    max_val = form.get('maxVal', '')
    log(min_val, max_val)
    data_list = []
    if total_digit(min_val) and total_digit(max_val):
        a = int(min_val)
        b = int(max_val)
        if a > b:
            a, b = b, a
        conn = sqlite3.connect('db.sqlite')
        c = conn.cursor()
        c.execute(
            'SELECT * FROM departments WHERE PRICE<{} AND PRICE>{}'.format(b, a)
        )
        # log(c.fetchall())
        for i in c.fetchall():
            data = {
                "address": i[2],
                "href": i[3],
            }
            data_list.append(data)
        conn.close()
    else:
        data = dict(address='八宝山')
        data_list.append(data)
    return jsonify(data_list)


if __name__ == '__main__':
    app.run(debug=True)