# -*- coding: utf-8 -*-
from flask import render_template, request, session, redirect, flash, url_for, jsonify
import json

from . import news

from .. import db
from ..models import News 
from ..common import nocache

from datetime import datetime as dt
import re

@news.route('/admin/news/new', methods=['POST'])
def new():
  f = request.form
  msg_arr = check_news_form(f)
  messages = ""

  if len(msg_arr)==0:
    if add_news_to_db(f):
      status = 200
      messages = u"成功添加新闻！"
    else:
      status = 500
      messages = u"添加新闻失败！"
  else:
    status = 500
    msg_arr = map(lambda x: x[1:], msg_arr)
    messages='<br>'.join(msg_arr)
  return jsonify({'status': status , 'message': messages})

def add_news_to_db(form):

  f = request.form

  n = News(subject=f['subject'],
           body=f['news'],
           created_at=dt.now(),
           updated_at=dt.now())
  db.session.add(n)
  db.session.commit()

  return True

def check_news_form(form):
  message = []

  subject = form['subject'].strip()
  body=form['news'].strip()

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
  elif len(body) > 8000:
    message.append(u'正文长度须少于8000个字符！')
  else:
    pass
    
  return message

@news.route('/admin/news/edit',methods=['POST'])
def edit():
  f = request.form
  msg_arr = check_news_form(f)
  messages = ""

  if len(msg_arr)==0:
    if update_news_to_db(f):
      status = 200
      messages = u"成功更新新闻：%s" % f['id']
    else:
      status = 500
      messages = u"更新新闻失败：%s" % f['id']
  else:
    status = 500
    msg_arr = map(lambda x: x[1:], msg_arr)
    messages='<br>'.join(msg_arr)
  return jsonify({'status': status , 'message': messages})

def update_news_to_db(form):

  f = request.form

  n = News.query.filter_by(id=int(f['id'])).first()

  n.subject=f['subject']
  n.body=f['news']
  n.updated_at=dt.now()

  db.session.add(n)
  db.session.commit()

  return True

@news.route('/admin/news/delete', methods=['POST'])
def delete():
  f = request.form

  n = News.query.filter_by(id=int(f['id'])).first()
  db.session.delete(n)
  db.session.commit()

  status = 200
  messages = u"成功删除新闻：%s" % f['id']
  return jsonify({'status': status , 'message': messages})

@news.route('/admin/news/list', methods=['GET'])
def list():
  (pagination, n_list) =get_list(request)
  return render_template('/news/list.html', n_list=n_list,  pagination=pagination)

@news.route('/news/list', methods=['GET'])
@news.route('/news/list.html', methods=['GET'])
def publish_list():
  (pagination, n_list) =get_list(request)
  return render_template('/news_list.html', n_list=n_list,  pagination=pagination)

@news.route('/news/latest_list', methods=['GET'])
@news.route('/news/latest_list.html', methods=['GET'])
def latest_list():
  (pagination, n_list) =get_list(request)
  return render_template('/news/latest_list.html', n_list=n_list)

def get_list(request):
  page = request.args.get('page')
  if page is None:
    page = 1
  else:
    page = int(page)
  pagination = News.query.order_by(News.created_at.desc()).paginate( \
      page, per_page=10, error_out=False)
  n_list = pagination.items
  return (pagination, n_list)

@news.route('/news/detail', methods=['GET'])
def detail():
  id = request.args.get('id')
  news = News.query.filter_by(id = int(id)).first()
  return render_template('/news_detail.html', news=news)
