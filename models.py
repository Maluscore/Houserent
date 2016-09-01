from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import sql

db_path = 'db.sqlite'
app = Flask(__name__)
app.secret_key = 'random string'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
db = SQLAlchemy(app)


class ReprMixin(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        return u'<{}: {}>'.format(class_name, self.id)


class Department(db.Model, ReprMixin):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    address = db.Column(db.String(10))
    href = db.Column(db.String())
    way = db.Column(db.String(4))
    price = db.Column(db.Integer)

    def __init__(self, form):
        self.title = form.get('title', '')
        self.address = form.get('address', '')
        self.href = form.get('href', '')
        self.way = form.get('way', '')
        self.price = form.get('price', '')

    def json(self):
        # Model 是延迟载入的, 如果没有引用过数据, 就不会从数据库中加载
        # 引用一下 id 这样数据就从数据库中载入了
        self.id
        d = {k: v for k, v in self.__dict__.items() if k not in self.blacklist()}
        return d

    def blacklist(self):
        b = [
            '_sa_instance_state',
        ]
        return b

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


if __name__ == '__main__':
    db.create_all()
    # print('创建成功')
