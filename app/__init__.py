from flask import Flask

def create_app():
    app = Flask(__name__)
    from .routes import task_bp
    app.register_blueprint(task_bp, url_prefix='/tasks')
    return app