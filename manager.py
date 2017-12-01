# -*- encoding=UTF-8 -*-

from lgblog import app, db
from flask_script import Manager
from sqlalchemy import or_, and_
from lgblog.models import *
from uuid import uuid4

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

    user = User(id=str(uuid4()), username='jmilkfan', password='fanguiju')
    db.session.add(user)
    db.session.commit()

    user = db.session.query(User).first()
    tag_one = Tag(id=str(uuid4()), name='Python')
    tag_two = Tag(id=str(uuid4()), name='Flask')
    tag_three = Tag(id=str(uuid4()), name='SQLALchemy')
    tag_four = Tag(id=str(uuid4()), name='JMilkFan')
    tag_list = [tag_one, tag_two, tag_three, tag_four]

    s = "EXAMPLE TEXT"

    for i in range(100):
        new_post = Post(id=str(uuid4()), title="Post" + str(i))
        new_post.user = user
        new_post.publish_date = datetime.datetime.now()
        new_post.text = s
        new_post.tags = random.sample(tag_list, random.randint(1, 3))
        db.session.add(new_post)

    db.session.commit()


if __name__ == '__main__':
    manager.run()
