from app import db
#from sqlalchemy import UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash


class News(db.Model):
  __tablename__ = 'news'
  id = db.Column(db.Integer, primary_key=True)
  subject = db.Column(db.Text, nullable=False)
  body = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, nullable=False)
  updated_at = db.Column(db.DateTime, nullable=False)

class Laws(db.Model):
  __tablename__ = 'laws'
  id = db.Column(db.Integer, primary_key=True)
  subject = db.Column(db.Text, nullable=False)
  category = db.Column(db.String(256), nullable=False)
  body = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, nullable=False)
  updated_at = db.Column(db.DateTime, nullable=False)

#Used for questions from the customer
#
class Question(db.Model):
  __tablename__ = 'questions'
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.Text, nullable=False)
  approved = db.Column(db.Boolean, default=False)
  created_at = db.Column(db.DateTime, nullable=False)
  updated_at = db.Column(db.DateTime, nullable=False)
  answers = db.relationship('Answer', backref='questions',lazy='dynamic')
  contact = db.relationship('Contact', backref='questions',lazy='select', uselist=False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id',  deferrable=True))
  # comment 15 add subject
  subject = db.Column(db.Text, nullable=False)
  category = db.Column(db.String(256), nullable=False)

class Answer(db.Model):
  __tablename__='answers'
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, nullable=True)
  updated_at = db.Column(db.DateTime, nullable=True)
  question_id = db.Column(db.Integer, db.ForeignKey('questions.id', deferrable=True))
  contact = db.relationship('Contact', backref='answers',lazy='select', uselist=False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id',deferrable=True))

class Contact(db.Model):
  __tablename__='contacts'
  id = db.Column(db.Integer, primary_key=True)
  display_name = db.Column(db.Text, nullable=True)
  remote_host = db.Column(db.String(15), default='0.0.0.0')
  telephone = db.Column(db.Text, nullable=True)
  qq = db.Column(db.Text, nullable=True)
  email = db.Column(db.Text, nullable=True)
  created_at = db.Column(db.DateTime, nullable=False)
  updated_at = db.Column(db.DateTime, nullable=False)
  question_id = db.Column(db.Integer, db.ForeignKey('questions.id',deferrable=True), nullable=True)
  answer_id = db.Column(db.Integer, db.ForeignKey('answers.id',deferrable=True), nullable=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id',deferrable=True))
##  UniqueConstraint('telephone', 'qq', 'email', name='contactonce')  
  #comment 15 add webchat, address, postcode
  wechat = db.Column(db.Text, nullable=True)
  address = db.Column(db.Text, nullable=True)
  postcode = db.Column(db.Text, nullable=True)

class User(db.Model):
  __tablename__='users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.Text, nullable=False, unique=True)
  password = db.Column(db.Text, nullable=False)
  password2 = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, nullable=False)
  updated_at = db.Column(db.DateTime, nullable=False)
  contact = db.relationship('Contact', backref='users',lazy='select', uselist=False)
  questions = db.relationship('Question', backref='users',lazy='dynamic')
  answers = db.relationship('Answer', backref='users',lazy='dynamic')

  @property
  def password(self):
    raise AttributeError('Password is not a readable attribute!')

  @password.setter
  def password(self, password):
    self.password2 = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.password2, password)
'''
class News(db.Model):
  __tablename__='news'

class Cases(db.Model):
  __tablename__='cases'

class Laws(db.Model):
  __tablename__='laws'

'''
