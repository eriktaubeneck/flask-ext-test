from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from ext import Extension


app = Flask(__name__)
app.config.update(
    {
        'SQLALCHEMY_DATABASE_URI': 'postgres://ext_test:@localhost:5432/ext_test',
        'EXTENSION_NAMESPACE': 'foobarbaz'
    }
)

db = SQLAlchemy(app)


class AppModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)


_ext = Extension(app, db)

if __name__ == '__main__':
    db.create_all()
    app.run(port=8230)
