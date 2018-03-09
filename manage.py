# -*- coding: utf-8 -*-
#!/opt/houhp/venv/bin/python


'''
 python manage.py db init|migrate|upgrade
'''

from flask.ext.script import Manager, Shell, Command
from flask.ext.migrate import Migrate, MigrateCommand
from datetime import datetime as dt

from app import app, db
from app.models import Question, Answer, Contact, User, News, Laws

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
  return dict(app=app, db=db, Question=Question, Answer=Answer, Contact=Contact, User=User, News=News, Laws=Laws)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

class InitialData(Command):
  "Initilize the db data"

  def run(self):
    admin_user = User(username='admin',
                      password='password',
                      password2='password',
                      created_at=dt.utcnow(),
                      updated_at=dt.utcnow())
    guest_user = User(username='guest',
                      password='password',
                      password2='password',
                      created_at=dt.utcnow(),
                      updated_at=dt.utcnow())
    db.session.add_all([admin_user, guest_user])
    db.session.commit()
    '''
    dummy_question = Question(body='dummy', 
                      user_id=guest_user.id,
                      created_at=dt.utcnow(),
                      updated_at=dt.utcnow())
    dummy_answer = Answer(body='dummy',
                      question_id=dummy_question.id,
                      user_id=admin_user.id,
                      created_at=dt.utcnow(),
                      updated_at=dt.utcnow())
    dummy_contact = Contact(question_id=dummy_question.id,
                      answer_id=dummy_answer.id,
                      user_id=guest_user.id,
                      created_at=dt.utcnow(),
                      updated_at=dt.utcnow())
    db.session.add_all([dummy_question,dummy_answer])
    db.session.commit()
    dummy_contact = Contact(question_id=dummy_question.id,
                      answer_id=dummy_answer.id,
                      user_id=guest_user.id,
                      created_at=dt.utcnow(),
                      updated_at=dt.utcnow())
    db.session.add_all([dummy_contact])
    db.session.commit()
    '''
manager.add_command("init_data", InitialData())

if __name__=="__main__":
  manager.run()
