from distutils.debug import DEBUG
class Config:
    SECRET_KEY = 'iwO)Sqo.1e0*@1Jk'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = '192.168.31.167'
    MYSQL_USER = 'root3'
    MYSQL_PASSWORD = 'ServidorPortaEnergia'
    MYSQL_DB = 'flask_login'


config =  {
    'production': DevelopmentConfig
}