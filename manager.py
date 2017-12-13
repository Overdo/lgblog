# -*- encoding=UTF-8 -*-

from lgblog import app, db
from flask_script import Manager
from sqlalchemy import or_, and_
from lgblog.models import *
from uuid import uuid4
from flask_principal import Permission, RoleNeed

manager = Manager(app)


@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    return dict(app=app,
                db=db,
                User=User,
                Post=Post,
                Comment=Comment,
                Role=Role
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

    user = User(id=str(uuid4()), username='jmilkfan', password='overdo')
    db.session.add(user)
    db.session.commit()

    user = db.session.query(User).first()
    tag_one = Tag(id=str(uuid4()), name='Python')
    tag_two = Tag(id=str(uuid4()), name='Flask')
    tag_three = Tag(id=str(uuid4()), name='SQLALchemy')
    tag_four = Tag(id=str(uuid4()), name='JMilkFan')
    tag_five = Tag(id=str(uuid4()), name='C++')
    tag_6 = Tag(id=str(uuid4()), name='JAVA')
    tag_7 = Tag(id=str(uuid4()), name='golang')
    tag_8 = Tag(id=str(uuid4()), name='fuck')
    tag_list = [tag_one, tag_two, tag_three, tag_four, tag_five, tag_6, tag_7, tag_8]

    # 这里设定了 3 种权限, 这些权限会被绑定到 Identity 之后才会发挥作用.
    # Init the role permission via RoleNeed(Need).
    role_admin = Role(id=str(uuid4()), name="admin")
    role_poster = Role(id=str(uuid4()), name="poster")
    role_default = Role(id=str(uuid4()), name="default")
    role_poster.users = [user]
    role_admin.users = [user]

    catagory1 = Category(id=str(uuid4()), name='程序员之殇')
    catagory2 = Category(id=str(uuid4()), name='产品经理之路')
    catagory3 = Category(id=str(uuid4()), name='我是美工')
    catagory4 = Category(id=str(uuid4()), name='闲言细语')
    catagory5 = Category(id=str(uuid4()), name='赚钱花花')

    catagory_list = [catagory1, catagory2, catagory3, catagory4, catagory5]

    db.session.add(catagory1)
    db.session.add(catagory2)
    db.session.add(catagory3)
    db.session.add(catagory4)
    db.session.add(catagory5)

    db.session.add(role_admin)
    db.session.add(role_poster)
    db.session.add(role_default)
    db.session.commit()

    for i in range(100):
        new_post = Post(id=str(uuid4()), title="Post" + str(i))
        new_post.user_id = user.id
        new_post.publish_date = datetime.datetime.now()
        new_post.text = 'this is example textbalabalabsakdhjaslkdjlsajdljasldjlaskjdlasjdlkajslkdjasldjlaskjdlasjdlkasjdlkasjdlkasjdlkjsaldkjaslkdjlkasjdlaskjdlaskjdlasjdlkasjslkdjasldjlaskjdlasjdlkasjdlkasjdlkasjdlkjsaldkjaslkdjlkasjdlaskjdlaskjdlasjdlkasjslkdjasldjlaskjdlasjdlkasjdlkasjdlkasjdlkjsaldkjaslkdjlkasjdlaskjdlaskjdlasjdlkasjslkdjasldjlaskjdlasjdlkasjdlkasjdlkasjdlkjsaldkjaslkdjlkasjdlaskjdlaskjdlasjdlkasjslkdjasldjlaskjdlasjdlkasjdlkasjdlkasjdlkjsaldkjaslkdjlkasjdlaskjdlaskjdlasjdlkasjd'
        new_post.tags = random.sample(tag_list, random.randint(1, 3))
        new_post.category_id = catagory_list[random.randint(0, 4)].id
        db.session.add(new_post)

    db.session.commit()


if __name__ == '__main__':
    manager.run()
