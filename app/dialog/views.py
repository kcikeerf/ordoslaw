# -*- coding: utf-8 -*-
from flask import render_template, request

from . import dialog
from ..models import Question, Answer, News, Laws

#question
#
@dialog.route('/admin/dialog/question/new', methods=['GET'])
@dialog.route('/admin/dialog/question/new.html', methods=['GET'])
def question_new():
  return render_template('/dialog/question/new.html')

@dialog.route('/admin/dialog/question/approve', methods=['GET'])
@dialog.route('/admin/dialog/question/approve.html', methods=['GET'])
def question_approve():
  id = request.args.get('id')
  q = Question.query.filter_by(id=id).first()
  return render_template('/dialog/question/approve.html', question=q)  

@dialog.route('/admin/dialog/question/delete', methods=['GET'])
@dialog.route('/admin/dialog/question/delete.html', methods=['GET'])
def question_delete():
  id = request.args.get('id')
  q = Question.query.filter_by(id=id).first()
  return render_template('/dialog/question/delete.html', question=q)

@dialog.route('/admin/dialog/question/edit', methods=['GET'])
@dialog.route('/admin/dialog/question/edit.html', methods=['GET'])
def question_edit():
  id = request.args.get('id')
  q = Question.query.filter_by(id=id).first()
  return render_template('/dialog/question/edit.html', question=q)

#answer
#
@dialog.route('/admin/dialog/answer/new', methods=['GET'])
@dialog.route('/admin/dialog/answer/new.html', methods=['GET'])
def answer_new():
  q_id = request.args.get('q_id')
  return render_template('/dialog/answer/new.html', q_id = q_id)

@dialog.route('/admin/dialog/answer/edit', methods=['GET'])
@dialog.route('/admin/dialog/answer/edit.html', methods=['GET'])
def answer_edit():
  id = request.args.get('id')
  a = Answer.query.filter_by(id=id).first()
  return render_template('/dialog/answer/edit.html', answer = a)

@dialog.route('/admin/dialog/answer/delete', methods=['GET'])
@dialog.route('/admin/dialog/answer/delete.html', methods=['GET'])
def answer_delete():
  id = request.args.get('id')
  a = Answer.query.filter_by(id=id).first()
  return render_template('/dialog/answer/delete.html', answer = a)

#news
#
@dialog.route('/admin/dialog/news/new', methods=['GET'])
@dialog.route('/admin/dialog/news/new.html', methods=['GET'])
def news_new():
  return render_template('/dialog/news/new.html')

@dialog.route('/admin/dialog/news/edit', methods=['GET'])
@dialog.route('/admin/dialog/news/edit.html', methods=['GET'])
def news_edit():
  id = request.args.get('id')
  n = News.query.filter_by(id=id).first()
  return render_template('/dialog/news/edit.html', news = n)

@dialog.route('/admin/dialog/news/delete', methods=['GET'])
@dialog.route('/admin/dialog/news/delete.html', methods=['GET'])
def news_delete():
  id = request.args.get('id')
  n = News.query.filter_by(id=id).first()
  return render_template('/dialog/news/delete.html', news = n)

@dialog.route('/admin/dialog/laws/new', methods=['GET'])
@dialog.route('/admin/dialog/laws/new.html', methods=['GET'])
def laws_new():
  return render_template('/dialog/laws/new.html')

#laws
@dialog.route('/admin/dialog/laws/edit', methods=['GET'])
@dialog.route('/admin/dialog/laws/edit.html', methods=['GET'])
def laws_edit():
  id = request.args.get('id')
  l = Laws.query.filter_by(id=id).first()
  return render_template('/dialog/laws/edit.html', laws = l)

@dialog.route('/admin/dialog/laws/delete', methods=['GET'])
@dialog.route('/admin/dialog/laws/delete.html', methods=['GET'])
def laws_delete():
  id = request.args.get('id')
  l = Laws.query.filter_by(id=id).first()
  return render_template('/dialog/laws/delete.html', laws = l)

