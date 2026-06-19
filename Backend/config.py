
class Config:
    SECRET_KEY = 'SECRETEKEYFORAPP2'
    SQLALCHEMY_DATABASE_URI = 'postgresql://neondb_owner:npg_ywaJNg2OMm6r@ep-twilight-frost-at8sjdok-pooler.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
    SECURITY_PASSWORD_SALT='SOMESALTTOTASTEAPP'
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    CACHE_TYPE = 'RedisCache'
    REDIS_URL ='rediss://default:gQAAAAAAAVpaAAIgcDJhNTVkZDhmMzM3YmQ0N2E2YTkzMTgzOGFmMmRlN2ZjYg@heroic-peacock-88666.upstash.io:6379'
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT=300
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_USE_TLS= False
    MAIL_USE_SSL = False 
    MAIL_USERNAME=None
    MAIL_PASSWORD = None 
    MAIL_DEFAULT_SENDER='admin@gmail.com'

