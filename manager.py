# -*- encoding=UTF-8 -*-

from lgblog import app, db, models
from flask_script import Manager
from sqlalchemy import or_, and_

manager = Manager(app)


@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    return dict(app=app,
                db=db,
                User=models.User,
                Post=models.Post,
                Comment=models.Comment
                )


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
