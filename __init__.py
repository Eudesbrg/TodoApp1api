import os
from flask import Flask
from flask_cors import CORS


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_URI=os.path.join(app.instance_path,'api.sqlite'),
        KEYCLAOK_URI="http://192.168.2.56:8080/",
        KEYCLOAK_REALM_NAME="keycloak"
    )

    if test_config is None : 
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py',silent=True)
    else:
        # load the instance config if it is pass
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    from . import db
    db.init_app(app)

    from . import todo
    app.register_blueprint(todo.bp)

    # test route
    @app.route('/hello')
    def hello():
        return "hello"
    
    return app
    
