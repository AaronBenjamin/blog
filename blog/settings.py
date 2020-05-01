import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', b'l\x9b\xf6\xd63\x90\xd9\xb5\x040\x83\xa7\x89\xdf')
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_HEIGHT = '800'
    CKEDITOR_FILE_UPLOADER = 'admin.upload_image'
    

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = ('BLOG Admin', MAIL_USERNAME)

    BLOG_EMAIL = os.getenv('BLOG_EMAIL')
    BLOG_POST_PER_PAGE = 6
    BLOG_MANAGE_POST_PER_PAGE = 15
    BLOG_SLOW_QUERY_THRESHOLD = 1

    BLOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    BLOG_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
    WHOOSHEE_MIN_STRING_LEN = 2


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', os.path.join(basedir, 'data-dev.db'))


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', os.path.join(basedir, 'data.db'))


config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig
}
