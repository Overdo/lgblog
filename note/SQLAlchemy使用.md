
### Flask-SQLAlchemy的介绍

1. ORM：Object Relationship Mapping（模型关系映射）
2. Flask-SQLAlchemy是一套ORM框架
3. ORM的好处：可以让我们操作数据库跟直接操作对象一样，非常方便，因为一个表能够抽象成一个类，一条数据可以抽象成类的一个对象

### Flask-SQLAlchemy的使用

1. 初始化和设置数据库配置信息：
   使用flask-sqlalchemy中的SQLAlchemy进行初始化
       from flask_sqlalchemy import SQLAlchemy
       app = Flask(__name__)
       db = SQLAlchemy(app)

2. 设置配置信息：在config.py文件中添加以下配置信息：
       # dialect+driver://user:password@host:port/database
       DIALECT = 'mysql'
       DRIVER = 'pymysql'
       USERNAME = 'root'
       PASSWORD = '123'
       HOST = '127.0.0.1'
       PORT = '3306'
       DATABASE = 'db_demo'
      
       SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
       SQLALCHEMY_TRACK_MODIFICATIONS = False
3. 在主app文件中添加配置文件

    app = Flask(__name__)
    app.config.from_object(config)
    db = SQLAlchemy(app)

4. 测试检查有无问题

    db.create_all()

有问题再做相应的修改

### 使用flask-SQLAlchemy创建模型与表的映射

1. 模型需要继承自db.Model,然后需要映射到表中的属性，必须写成db.Column的数据类型
2. 数据类型：
   - db.Integer代表的是整形
   - db.String代表的是varchar，需要指定长度
   - db.Text代表的是text
   - 等等
3. 其他参数：
   - primary_key
   - auyoincrement
   - nullable
   - 等等
4. 最后调用db.create_all来将模型真正的创建到数据库中

### Flask-SQLAlchemy的增删改查

1. 增：
       @app.route('/add/')
       def add():
           arcticle = Article(title='add test', content='hahahahhaha')
           db.session.add(arcticle)
           db.session.commit()
           return ''
2. 删：
       @app.route('/delete/')
       def delete():
           article = Article.query.filter(Article.title == 'add test').first()
           db.session.delete(article)
           db.session.commit()
           return 'deleted'
3. 改：
       @app.route('/update/')
       def update():
           article = Article.query.filter(Article.title == 'add test').first()
           article.title = 'alkasjdlasjdlkjalsdlasjdl'
           db.session.commit()
           return article.title
4. 查
       @app.route('/search/')
       def search():
           # select * from article where title = 'add test'
           article = Article.query.filter(Article.title == 'add test').first()
           print(article.title+article.content)
           return article.title+article.content

### Flask-SQLAlchemy外键及其关系

1. 外键``
       class User(db.Model):
           __tablename__ = 'user'
           id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
           username = db.Column(db.String(100), nullable=False)
      
       class Article(db.Model):
      
           __tablename__ = 'article'
           id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
           title = db.Column(db.String(100), nullable=False)
           content = db.Column(db.TEXT, nullable=False)
           author_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
           author = db.relationship('User', backref=db.backref('articles'))

    2. `author = db.relationship('User', backref=db.backref('articles'))`解释：

       * 给Acticle这个模型增加一个author 属性，可以访问这篇文章作者的数据，想访问普通模型属性一样
       * backref是定义一个反向引用，可以通过User.article访问这个模型所写的所有文章

    3. 多对多：

       * 多对多的关系，需要通过一个中间表进行关联

       * 中间表不能通过class的方式实现，只能通过db.Table的方式实现

       * 设置关联：`tags = db.relationship('Tag', secondary=article_tag. backref=backref('articles'))`需要使用一个关键字参数`secondary=中间表`来进行关联。

       * 格式如下：

         ```python
         # 多对多必须的中间关联表
         posts_tags = db.Table('posts_tags',
                               db.Column('post_id', db.String(45),db.ForeignKey('posts.id')),
                               db.Column('tag_id', db.String(45), db.ForeignKey('tags.id')))


         class Post(db.Model):
             """Represents Proected posts."""

             __tablename__ = 'posts'
             id = db.Column(db.String(45), primary_key=True)
             title = db.Column(db.String(255))
             text = db.Column(db.Text())
             publish_date = db.Column(db.DateTime)
             # ------------------------------------------------------------------
             # Set the foreign key for Post
             user_id = db.Column(db.String(45), db.ForeignKey('users.id'))

             # Establish relationship many to many: posts <==> tags
             tags = db.relationship('Tag',
                                    secondary='posts_tags',
                                    lazy='dynamic')
           	# ------------------------------------------------------------------
             def __init__(self, title):
                 self.title = title

             def __repr__(self):
                 return "<Model Post `{}`>".format(self.title)
                 
           class Tag(db.Model):
             """Represents Proected tags."""

             __tablename__ = 'tags'
             id = db.Column(db.String(45), primary_key=True)
             name = db.Column(db.String(255))


             posts = db.relationship('Post',
                                     secondary='posts_tags',
                                     lazy='dynamic')

             def __init__(self, name):
                 self.name = name

             def __repr__(self):
                 return "<Model Tag `{}`>".format(self.name)
         ```

         ​

    4. ​









