# -*- coding: utf-8 -*-
from flask import render_template, request, session, redirect, flash, url_for, jsonify
import json

from . import question
from .. import db
from ..models import Question, Answer, Contact, User
from ..common import nocache

from datetime import datetime as dt
import re

@question.route('/question/new', methods=['GET', 'POST'])
def create_question():
  target_template = 'question/new.html'
  if request.method == 'GET':
    return render_template(target_template)
  elif request.method == 'POST':
    if session.has_key('last_question_submit') \
       and session['last_question_submit'] is not None \
       and len(session['last_question_submit']) > 0:
       interval = (dt.now() - dt.strptime(session['last_question_submit'], '%Y/%m/%d %H:%M:%S')).seconds
    else:
       interval = 180
    
    if interval >= 180:  
      messages = check_question_form(request.form)

      #check verify code
      if len(request.form['verifycode']) == 0:
        messages.append(u'w请输入验证码')
      elif request.form['verifycode'] != session['verifycode']:
        messages.append(u'w请输入正确的验证码!')
      else:
        pass
    else:
      messages=[u'w您的请求提交过于频繁，3分钟内只能提交一次！']

    for m in messages:
      flash(m)
    if len(messages)==0:
      if add_question_to_db(request):
        flash(u'i您的咨询信息已成功提交，我们会尽快进行解答，请关注“免费法律咨询”栏目！')
        session['last_question_submit']=dt.now().strftime('%Y/%m/%d %H:%M:%S')
        return render_template("question/success.html")
        #redirect(url_for('/main/zaixianfalv', _external=True))
      else:
        flash(u'e问题提交过程中出现问题，请联系网站管理员!')

    return render_template(target_template, form=request.form)
  else:
    return 'not found'

#from admin console
@question.route('/admin/question/new', methods=['POST'])
def new():
  f=request.form
  msg_arr = check_question_form(f)
  messages = ""
  if len(msg_arr)==0:
    if add_question_to_db(request):
      status = 200
      messages=u"成功添加法律咨询!"
    else:
      status = 500
      messages=u"添加法律咨询失败！"
  else:
    status = 500
    msg_arr = map(lambda x: x[1:], msg_arr)
    messages='<br>'.join(msg_arr)

  return jsonify({'status': status , 'message': messages})

def check_question_form(form):
  message = []

  display_name = form['display_name'].strip()
  qq=form['qq'].strip()
#  wechat=form['wechat'].strip()
  tel=form['telephone'].strip()
  email=form['email'].strip()
  address=form['address'].strip()
  postcode=form['postcode'].strip()
  subject=form['subject'].strip()  
  question=form['question'].strip()

  # check Name format
  #if len(display_name) == 0:
  #  message.append(u'w请输入您的名字！')
  if len(display_name) > 30:
    message.append(u'w名字长度须少于30个字符！')
  else:
    pass

  # check Contacts format
  if len(qq) !=  0:
    # check QQ format
    if len(qq) > 100:
      message.append(u'wQQ长度超过限制！请输入小于100字符！')
    elif len(qq) > 0 and re.match(r"^[0-9]{6,}$" , qq) is None:
      message.append(u'w请输入正确的QQ！')
    else:
      pass

  if len(tel) != 0:
    # check Tel format
    if len(tel) > 100: 
      message.append(u'w电话长度超过限制！请输入小于100字符！')
    elif len(tel) > 0 and re.match(r"^[0-9]{3,}$" , tel) is None:
      message.append(u'w请输入正确的电话！')
    else:
      pass

  if len(email) !=0:
    # check Email format
    if len(email) > 256:
      message.append(u'w邮箱长度超过限制！请输入小于256字符！')
    elif len(email) > 0 and re.match(r"^[^@]+@[^@]+\.[^@]+$" , email) is None:
      message.append(u'w请输入正确的邮箱！')
    else:
      pass

  if len(address) !=0:
    if len(address) > 256:
      message.append(u'w地址长度超过限制！请输入小于256字符！')
    else:
      pass

  if len(postcode) !=0:
    if len(postcode) > 15:
      message.append(u'w邮编长度超过限制！请输入小于15个字符！')
    else:
      pass

  # check subject format
  if len(subject) == 0:
    message.append(u'w请输入您的标题！')
  elif len(subject) <=5 :
    message.append(u'w您的标题过短请输入超过5个字符！')
  elif len(subject) > 80:
    message.append(u'w标题长度超过限制！请输入小于80个字符！')
  else:
    pass

  # check Question format
  if len(question) == 0:
    message.append(u'w请输入您的问题！')
  elif len(question) < 5:
    message.append(u'w您的问题过短请输入超过10个字符！')
  elif len(question) > 8000:
    message.append(u'w问题长度超过限制！请输入小于8000字符！')
  else:
    pass

  return message


def add_question_to_db(request):

  form = request.form

  # to be extended in the future
  guest = User.query.filter_by(username='guest').first()

  q = Question(category=form['category'],
               subject=form['subject'],
               body=form['question'],
               user_id=guest.id,
               created_at=dt.now(),
               updated_at=dt.now())
  db.session.add(q)
  db.session.commit()
  c = Contact(display_name=form['display_name'],
              email=form['email'],
              qq=form['qq'],
              wechat=form['wechat'],
              telephone=form['telephone'],
              address=form['address'],
              postcode=form['postcode'],
              remote_host = request.remote_addr,
              user_id=guest.id,
              question_id=q.id,
              created_at=dt.now(),
              updated_at=dt.now())
  db.session.add(c)
  db.session.commit()
  return True

@question.route('/admin/question/list', methods=['GET'])
def list():
  page = request.args.get('page')
  if page is None:
    page = 1
  else:
    page = int(page)
  pagination = Question.query.order_by(Question.created_at.desc()).paginate( \
      page, per_page=10, error_out=False)
  q_list = pagination.items
  return render_template('question/list.html', q_list=q_list, pagination=pagination)


@question.route('/question/latest_list', methods=['GET'])
@question.route('/question/latest_list.html', methods=['GET'])
def latest_list():
  (pagination, n_list) =get_list(request)
  return render_template('/question/latest_list.html', n_list=n_list)

def get_list(request):
  page = request.args.get('page')
  if page is None:
    page = 1
  else:
    page = int(page)
  pagination = Question.query.filter_by(approved=True).order_by(Question.created_at.desc()).paginate( \
      page, per_page=21, error_out=False)
  n_list = pagination.items
  return (pagination, n_list)

@question.route('/admin/question/approve', methods=['POST'])
def approve():
  id = request.form['id']
  if id:
    id = int(id)
  q= Question.query.filter_by(id=id).first()
  if q.approved:
    q.approved = False
  else:
    q.approved = True
  db.session.add(q)
  db.session.commit()
  status = 200
  message=u"成功更新问题： %d" % (q.id)
  return jsonify({'status': status , 'message': message})

@question.route('/admin/question/delete', methods=['POST'])
def delete():
  id = request.form['id']
  if id:
    id = int(id)
  q= Question.query.filter_by(id=id).first()
  db.session.delete(q)
  db.session.commit()
  status = 200
  message=u"成功删除问题： %d" % (q.id)
  return jsonify({'status': status , 'message': message})

@question.route('/admin/question/edit', methods=['POST'])
def edit():
  f = request.form
  msg_arr = check_question_form(f)
  messages=""
  if len(msg_arr)==0:
    if update_question_to_db(f):
      status = 200
      messages=u"成功更新问题： %s" % (f['id'])
    else:
      status = 500
      messages=u"更新数据到DB出现问题： %s" % (f['id'])
  else:
    status = 500
    msg_arr = map(lambda x: x[1:], msg_arr)  
    messages='<br>'.join(msg_arr)

  return jsonify({'status': status , 'message': messages})

def update_question_to_db(form):

  f = form
  q = Question.query.filter_by(id=int(f['id'])).first()

  q.category = f['category']
  q.subject =f['subject'] 
  q.body = f['question']
  q.updated_at = dt.now()

  db.session.add(q)
  db.session.commit()

  c = q.contact
  c.display_name=f['display_name']
  c.qq=f['qq']
  c.wechat=f['wechat']
  c.telephone=f['telephone']
  c.email=f['email']
  c.address=f['address']
  c.postcode=f['postcode']
  c.updated_at=dt.now()

  db.session.add(c)
  db.session.commit()
  return True

@question.route('/question/detail', methods=['GET'])
def detail():
  id = request.args.get('id')
  question = Question.query.filter_by(id = int(id)).first()
  return render_template('/question_detail.html', question=question)
