# -*- coding: utf-8 -*-
from flask import render_template, request, session, redirect, flash, url_for, jsonify
import json

from . import answer
from .. import db
from ..models import Question, Answer, Contact, User
from ..common import nocache

from datetime import datetime as dt
import re

@answer.route('/admin/answer/new', methods=['POST'])
def create():
  f = request.form
  msg_arr = check_answer_form(f)
  messages = ""

  if len(msg_arr)==0:
    if add_answer_to_db(f):
      status = 200
      messages = u"成功添加回复!"
    else:
      status = 500
      messages = u"添加回复失败!"
  else:
    status = 500
    msg_arr = map(lambda x: x[1:], msg_arr)
    messages='<br>'.join(msg_arr)

  return jsonify({'status': status , 'message': messages})  

def add_answer_to_db(form):

  try:
    f = form

    # to be extended in the future
    guest = User.query.filter_by(username='guest').first()

    a = Answer(body=f['answer'],
               user_id=guest.id,
               question_id=f['q_id'],
               created_at=dt.now(),
               updated_at=dt.now())
    db.session.add(a)
    db.session.commit()

    c = Contact(display_name=f['display_name'],
                email=f['email'],
                qq=f['qq'],
                telephone=f['telephone'],
                remote_host = request.remote_addr,
                user_id=guest.id,
                answer_id=a.id,
                created_at=dt.now(),
                updated_at=dt.now())
    db.session.add(c)
    db.session.commit()
  except Exception, e:
    print(e)
    return False
  return True

@answer.route('/admin/answer/edit', methods=['POST'])
def edit():
  f = request.form
  msg_arr = check_answer_form(f)
  messages = ""

  if len(msg_arr)==0:
    if update_answer_to_db(f):
      status = 200
      messages = u"成功修改回复：%s" % f['id']
    else:
      status = 500
      messages = u"修改回复失败：%s" % f['id']
  else:
    status = 500
    msg_arr = map(lambda x: x[1:], msg_arr)
    messages='<br>'.join(msg_arr)
  return jsonify({'status': status , 'message': messages})

def update_answer_to_db(form):

  f = form
  a = Answer.query.filter_by(id=int(f['id'])).first()

  a.body = f['answer']
  a.updated_at = dt.now()

  db.session.add(a)
  db.session.commit()

  c = a.contact
  c.display_name=f['display_name']
  c.qq=f['qq']
  c.telephone=f['telephone']

  return True

@answer.route('/admin/answer/delete', methods=['POST'])
def delete():
  id = request.form['id']
  if id:
    id = int(id)
  a= Answer.query.filter_by(id=id).first()
  db.session.delete(a)
  db.session.commit()
  status = 200
  message=u"成功删除问题： %d" % (a.id)
  return jsonify({'status': status , 'message': message})


def check_answer_form(form):
  message = []

  display_name = form['display_name'].strip()
  qq=form['qq'].strip()
  tel=form['telephone'].strip()
  email=form['email'].strip()
  answer=form['answer'].strip()

  # check Name format
  if len(display_name) == 0:
    message.append(u'w请输入您的名字！')
  elif len(display_name) > 30:
    message.append(u'w名字长度须少于30个字符！')
  else:
    pass

  # check Contacts format
  if len(qq) ==  0 and len(tel) == 0 and len(email) ==0:
     pass
     #message.append(u'w请您至少输入QQ, 电话, 邮箱中的任意一种联系方式!')
  else:
    # check QQ format
    if len(qq) > 100:
      message.append(u'wQQ长度超过限制！请输入小于100字符！')
    elif len(qq) > 0 and re.match(r"^[0-9]{6,}$" , qq) is None:
      message.append(u'w请输入正确的QQ！')
    else:
      pass

    # check Tel format
    if len(tel) > 100:
      message.append(u'w电话长度超过限制！请输入小于100字符！')
    elif len(tel) > 0 and re.match(r"^[0-9]{3,}$" , tel) is None:
      message.append(u'w请输入正确的电话！')
    else:
      pass

    # check Email format
    if len(email) > 256:
      message.append(u'w邮箱长度超过限制！请输入小于256字符！')
    elif len(email) > 0 and re.match(r"^[^@]+@[^@]+\.[^@]+$" , email) is None:
      message.append(u'w请输入正确的邮箱！')
    else:
      pass

  # check answer format
  if len(answer) == 0:
    message.append(u'w请输入您的问题！')
  elif len(answer) < 10:
    message.append(u'w您的问题过短请输入超过10个字符！')
  elif len(answer) > 8000:
    message.append(u'w问题长度超过限制！请输入小于8000字符！')
  else:
    pass

  return message
