from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index_view():
    return render_template('index.html')


@app.route('/gongyu', methods=['POST'])
def data_post():
    pass


if __name__ == '__main__':
    app.run(debug=True)