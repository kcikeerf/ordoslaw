from flask import render_template, request

from . import admin

@admin.route('/admin/', methods=['GET'])
@admin.route('/admin/index', methods=['GET'])
@admin.route('/admin/index.html', methods=['GET'])
def index():
  return render_template('admin/index.html')  

