#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_script import Manager
from flask_migrate import MigrateCommand

from Mandark.project import create_app, db


app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def recreate_db():
    """Recreates the database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    manager.run()
