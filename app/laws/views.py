# -*- coding: utf-8 -*-
from flask import render_template, request, session, redirect, flash, url_for, jsonify
import json

from . import laws

from .. import db
from ..models import Laws 
from ..common import nocache

from datetime import datetime as dt
import re

@laws.route('/admin/laws/new', methods=['POST'])
def new():
  f = request.form
  msg_arr = check_laws_form(f)
  messages = ""

  if len(msg_arr)==0:
    if add_laws_to_db(f):
      status = 200
      messages = u"成功添加法律记文！!"
    else:
      status = 500
      messages = u"添加法律法规失败!"
  else:
    status = 500
    msg_arr = map(lambda x: x[1:], msg_arr)
    messages='<br>'.join(msg_arr)

  return jsonify({'status': status , 'message': messages})

def add_laws_to_db(form):

  f = form

  l = Laws(subject=f['subject'],
           category=f['category'],
           body=f['laws'],
           created_at=dt.now(),
           updated_at=dt.now())
  db.session.add(l)
  db.session.commit()

  return True


def check_laws_form(form):
  message = []

  subject = form['subject'].strip()
  body=form['laws'].strip()

  # check subject format
  if len(subject) == 0:
    message.append(u'请输入标题！')
  elif len(subject) > 256:
    message.append(u'标题长度须少于256个字符！')
  else:
    pass

  # check body format
  if len(body) == 0:
    message.append(u'请输入正文！')
#  elif len(body) > 4000:
#    message.append(u'正文长度须少于4000个字符！')
  else:
    pass
    
  return message

@laws.route('/admin/laws/edit',methods=['POST'])
def edit():
  f = request.form
  msg_arr = check_laws_form(f)
  messages = ""

  if len(msg_arr)==0:
    if update_laws_to_db(f):
      status = 200
      messages = u"成功更新法律法规: %d" % int(f['id'])
    else:
      status = 500
      messages = u"更新法律法规失败: %d" % int(f['id'])
  else:
    status = 500
    msg_arr = map(lambda x: x[1:], msg_arr)
    messages='<br>'.join(msg_arr)

  return jsonify({'status': status , 'message': messages})

def update_laws_to_db(form):

  f = form
  l = Laws.query.filter_by(id=int(f['id'])).first()

  l.subject = f['subject']
  l.category = f['category']
  l.body = f['laws']
  l.updated_at = dt.now()

  db.session.add(l)
  db.session.commit()

  return True


@laws.route('/admin/laws/delete', methods=['POST'])
def delete():
  id = request.form['id']
  if id:
    id = int(id)
  l = Laws.query.filter_by(id=id).first()
  db.session.delete(l)
  db.session.commit()
  status = 200
  messages = u"成功删除法律记文: %s" % id
  return jsonify({'status': status , 'message': messages})

@laws.route('/admin/laws/list', methods=['GET'])
def list():
  (pagination, l_list) = get_list(request)
  return render_template('/laws/list.html', l_list=l_list,  pagination=pagination)

@laws.route('/laws/list', methods=['GET'])
@laws.route('/laws/list.html', methods=['GET'])
def publish_list():
  (pagination, l_list) = get_list(request)
  category = request.args.get('category')
  return render_template('/laws_list.html', category=category, \
    l_list=l_list,  pagination=pagination)

@laws.route('/laws/latest_list', methods=['GET'])
@laws.route('/laws/latest_list.html', methods=['GET'])
def latest_list():
  (pagination, l_list) =get_list(request)
  return render_template('/laws/latest_list.html', l_list=l_list)

def get_list(request):
  page = request.args.get('page')
  if page is None:
    page = 1
  else:
    page = int(page)

  category = request.args.get('category')
  if category:
    pagination = Laws.query.filter_by(category = category).order_by(Laws.updated_at.desc()).paginate( \
        page, per_page=10, error_out=False)
  else:
    pagination = Laws.query.order_by(Laws.created_at.desc()).paginate( \
        page, per_page=10, error_out=False)
  l_list = pagination.items

  return (pagination, l_list)

@laws.route('/laws/detail', methods=['GET'])
def detail():
  id = request.args.get('id')
  law = Laws.query.filter_by(id = int(id)).first()
  return render_template('/laws_detail.html', law=law)
