import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
  SECRET_KEY=os.environ.get('SECRET_KEY') or 'qi tian da sheng'
  SQLALCHEMY_COMMIT_ON_TEARDOWN = True

  @staticmethod
  def init_app(app):
    pass

class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + basedir  + '/db/development.sqlite'

class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + basedir + '/db/test.sqlite'

class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + basedir + '/db/product.sqlite'

config = {
  'development': DevelopmentConfig,
  'testing': TestingConfig,
  'production': ProductionConfig,
  'default': DevelopmentConfig
}

