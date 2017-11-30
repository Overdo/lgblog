# -*- encoding=UTF-8 -*-

from lgblog import app, db
from flask_script import Manager
from sqlalchemy import or_, and_
from lgblog.models import *

manager = Manager(app)


@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    return dict(app=app,
                db=db,
                User=User)


@manager.command
def run_test():
    # init_database()
    db.drop_all()
    db.create_all()
    tests = unittest.TestLoader().discover('./')
    unittest.TextTestRunner().run(tests)


@manager.command
def init_database():
    db.drop_all()
    db.create_all()


if __name__ == '__main__':
    manager.run()
