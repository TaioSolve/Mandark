# -*- coding: utf-8 -*-
from flask_script import Manager
from flask_migrate import MigrateCommand

from Mandark.project import create_app, db


app = create_app()
manager = Manager()
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
