from flask import current_app, Blueprint
from flask.ext.sqlalchemy import sqlalchemy as sa

extension_bp = Blueprint('index', __name__, url_prefix='/ext')


@extension_bp.route('/', methods=('GET',))
def index():
    return 'hello ext'


@extension_bp.route('/echo/<content>', methods=('GET',))
def echo(content):
    return content


class ExtensionModelBase(object):
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.Text)


class Extension(object):
    def __init__(self, app=None, db=None):
        if app:
            self._app = app
        if app and db:
            return self.init_app(app, db)

    def init_app(self, app, db):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions.update(
            {
                'extension': self,
                'db': db,
            }
        )
        self.init_models()
        self.init_blueprints()

    @property
    def app(self):
        if hasattr(self, '_app'):
            return self._app
        return current_app

    @property
    def db(self):
        return self.app.extensions['db']

    def config(self, key, default=None):
        if default:
            return self.app.config.get(
                'EXTENSION_{}'.format(key.upper()),
                default
            )
        return self.app.config['EXTENSION_{}'.format(key.upper())]

    @property
    def namespace(self):
        return self.config('namespace', 'extension')

    def init_models(self):
        class ExtensionModel(self.db.Model, ExtensionModelBase):
            __tablename__ = '{}_model'.format(self.namespace)

    def init_blueprints(self):
        extension_bp.name = '{}.index'.format(self.namespace)
        extension_bp.url_prefix = '/{}'.format(self.namespace)
        self.app.register_blueprint(extension_bp)
