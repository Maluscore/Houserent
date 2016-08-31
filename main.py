from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from utils import log

app = Flask(__name__)


@app.route('/')
def index_view():
    return render_template('index.html')


@app.route('/gongyu', methods=['POST'])
def data_post():
    form = request.get_json()
    min_val = form.get('minVal', '')
    max_val = form.get('maxVal', '')
    log(min_val)
    data_list = []
    data = dict(address='天安门')
    data_list.append(data)
    return jsonify(data_list)


if __name__ == '__main__':
    app.run(debug=True)