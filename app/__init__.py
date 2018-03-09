# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_assets import Bundle, Environment

from config import config

app = Flask(__name__)
#should change to product when code finished
app.config.from_object(config['production'])
config['development'].init_app(app)

#database
db = SQLAlchemy()
db.init_app(app)

#javascript, css
assets = Environment(app)
bundles = {
  'base_js': Bundle(
#    'js/jquery-1.2.1.pack.js',
    'js/jquery-1.11.3.min.js',
    'js/jquery-easyui/jquery.easyui.min.js',
    'js/jquery.qrcode-0.12.0.min.js',
#    'js/jquery.qrcode.min.js',
    'js/mine.js',
    'js/menu.js',
#    'js/nav.js'
#    output='base.js'
  ),
  'admin_js': Bundle(
    'js/jquery-1.11.3.min.js',
    'js/jquery-easyui/jquery.easyui.min.js',
    'js/admin.js',
    'js/dialog.js'
  ),
  'base_css': Bundle(
    'js/jquery-easyui/themes/default/easyui.css',
    'js/jquery-easyui/themes/icon.css',
    'js/jquery-easyui/demo/demo.css',
    'css/css.css',
    'css/css2.css'
#    output='base.css'
  ),
  'admin_css': Bundle(
    'js/jquery-easyui/themes/default/easyui.css',
    'js/jquery-easyui/themes/icon.css',
    'js/jquery-easyui/demo/demo.css',
    'css/css.css',
    'css/css2.css',
    'css/mine.css'
  )
}
assets.register(bundles)

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)
from .question import question as question_blueprint
app.register_blueprint(question_blueprint)
from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)
from .dialog import dialog as dialog_blueprint
app.register_blueprint(dialog_blueprint)
from .answer import answer as answer_blueprint
app.register_blueprint(answer_blueprint)
from .news import news as news_blueprint
app.register_blueprint(news_blueprint)
from .laws import laws as laws_blueprint
app.register_blueprint(laws_blueprint)



if __name__ == "__main__":
    app.run()

