# -*- coding: utf-8 -*-
from flask import render_template, request, session, redirect, make_response
from . import main

from ..models import Question
from ..common import create_validate_code

import StringIO

@main.route('/', methods=['GET'])
@main.route('/index', methods=['GET'])
@main.route('/index.html', methods=['GET'])
def index():
  return render_template('index.html')

@main.route('/robots.txt', methods=['GET'])
def robots():
  return render_template('robots.txt')


@main.route('/zaixianfalv.html', methods=['GET'])
@main.route('/zaixianfalv', methods=['GET'])
def zaixianfalv():
  page = request.args.get('page')
  if page is None:
    page = 1
  else:
    page = int(page)
  pagination = Question.query.filter_by(approved=True).order_by(Question.created_at.desc()).paginate( \
      page, per_page=10, error_out=False)
  q_list = pagination.items
  return render_template('zaixianfalv.html', q_list=q_list, pagination=pagination)

@main.route('/getcode', methods=['GET'])
def get_code():
  code_img,strs = create_validate_code()
  session["verifycode"]=strs
  buf = StringIO.StringIO()
  code_img.save(buf,'JPEG',quality=70)

  buf_str = buf.getvalue()
  response = make_response(buf_str)
  response.headers['Content-Type'] = 'image/jpeg'
  return response

@main.route('/aboutus', methods=['GET'])
@main.route('/aboutus.html', methods=['GET'])
def aboutus():
  return render_template('aboutus.html')

