# -*- encoding=UTF-8 -*-

from lgtalk import app, db
from flask_script import Manager
from sqlalchemy import or_, and_
from lgtalk.models import *

manager = Manager(app)


def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'


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

    for i in range(1, 101):
        db.session.add(User('User' + str(i), 'a' + str(i)))
        for j in range(1, 11):
            db.session.add(Article('title' + str(j), 'This is a article ' + str(i) + str(j), i))
            for k in range(0, 3):
                db.session.add(Comment('This is a comment' + str(i) + str(j) + str(k), i))

    db.session.commit()

    #
    # print 1, User.query.all()
    print(2, User.query.get(3))
    print(3, Article.query.filter_by(id=5).first().content)
    print(4, User.query.order_by(User.id.desc()).offset(1).limit(2).all())
    # print 5, User.query.filter(User.username.endswith('0')).limit(3).all()
    # print 6, User.query.filter(or_(User.id == 88, User.id == 99)).all()
    # print 7, User.query.filter(and_(User.id > 88, User.id < 93)).all()
    # print 8, User.query.filter(and_(User.id > 88, User.id < 93)).first_or_404()
    # print 9, User.query.order_by(User.id.desc()).paginate(page=1, per_page=10).items
    # user = User.query.get(1)
    # print 10, user.images
    #
    #
    #
    # image = Image.query.get(1)
    # print 11, image, image.user


if __name__ == '__main__':
    manager.run()
