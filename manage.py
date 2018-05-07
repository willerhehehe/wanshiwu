#encoding:utf-8

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from wanshiwu import app
from exts import db
from models import User

'''
若使用python3,不支持mysqldb,需要使用pymysql替代：pip install pymysql
在sqlalchemy下的init.py中写入以下两行 
import pymysql
pymysql.install_as_MySQLdb()

数据库命令：
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
'''
manager = Manager(app)

#使用Migrate绑定app和db
migrate = Migrate(app,db)

#添加迁移脚本的命令到manager中
manager.add_command('db',MigrateCommand)

if __name__ == "__main__":
    manager.run()


