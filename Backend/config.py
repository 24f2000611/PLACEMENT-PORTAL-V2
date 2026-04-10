
class Config:
    SECRET_KEY = 'SECRETEKEYFORAPP2'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///placement.db'
    SECURITY_PASSWORD_SALT='SOMESALTTOTASTEAPP'
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = 'redis://localhost:6379/0'
    CACHE_DEFAULT_TIMEOUT=300
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_USE_TLS= False
    MAIL_USE_SSL = False 
    MAIL_USERNAME=None
    MAIL_PASSWORD = None 
    MAIL_DEFAULT_SENDER='admin@gmail.com'

