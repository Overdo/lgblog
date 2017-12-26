# -*- encoding=UTF-8 -*-
import os, re
from lgblog import app, db
from flask_script import Manager
from sqlalchemy import or_, and_
from lgblog.models import *
from uuid import uuid4
from flask_principal import Permission, RoleNeed
import datetime

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

    user = User(id=str(uuid4()), username='overdo', password='overdo')
    db.session.add(user)
    db.session.commit()

    # # 将原来博客内容迁移到此
    # dir = 'D:\workspace\Overdo.github.io\_posts\\'
    # for file in os.listdir(dir):
    #     if file.startswith('2'):
    #         with open(dir + file, 'rb') as f:
    #             all = f.read().decode('utf-8')
    #
    #             reg = re.compile(
    #                 '---(.*?)layout:(.*?)title:(.*?)categories:(.*?)description:(.*?)keywords:(.*?)---(.*)', re.S)
    #             resoult = re.search(reg, all)
    #
    #             category = Category.query.filter_by(name=resoult.group(4)).first()
    #             if not category:
    #                 category = Category(id=str(uuid4()), name=resoult.group(4).strip())
    #             db.session.add(category)
    #             db.session.commit()
    #
    #             tags = []
    #             post_tags=[]
    #             temp = resoult.group(6).strip().split(',')
    #             for tag in temp:
    #                 tags.extend(tag.split('，'))
    #             for tag in tags:
    #                 q_tag = Tag.query.filter_by(name=tag).first()
    #                 if not q_tag:
    #                     q_tag = Tag(id=str(uuid4()), name=tag)
    #                     db.session.add(q_tag)
    #                     db.session.commit()
    #                 post_tags.append(q_tag)
    #
    #             new_post = Post(id=str(uuid4()), title=resoult.group(3).strip())
    #             new_post.user_id = user.id
    #             new_post.publish_date = datetime.datetime.now()
    #             new_post.text = resoult.group(7).strip()
    #             new_post.tags = post_tags
    #             new_post.category_id = category.id
    #
    #             db.session.add(new_post)
    #             db.session.commit()



    user = db.session.query(User).first()
    tag_one = Tag(id=str(uuid4()), name='Python')
    tag_two = Tag(id=str(uuid4()), name='Flask')
    tag_three = Tag(id=str(uuid4()), name='SQLALchemy')
    tag_four = Tag(id=str(uuid4()), name='Overdo')
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
        new_post = Post(id=str(uuid4()), title="谈谈CSRF漏洞")
        new_post.user_id = user.id
        new_post.publish_date = datetime.datetime.now()
        new_post.text = '''
        #### CSRF概念

​	先说说什么是CSRF（Cross—Site Request Forgery），顾名思义，跨站请求伪造，也就是：攻击者盗用了你的身份，以你的名义发送邮件、发消息，盗取你的账号，添加系统管理员，甚至于购买商品、虚拟货币转账等。 

#### CSRF原理过程

​	假设Web A为存在CSRF漏洞的网站，Web B为攻击者构建的恶意网站，User C为Web A网站的合法用户。进行CSRF攻击的原理及过程如下：

1. 用户C打开浏览器，访问受信任网站A，输入用户名和密码请求登录网站A；
2. 在用户信息通过验证后，网站A产生Cookie信息并返回给浏览器，此时用户登录网站A成功，可以正常发送请求到网站A；
3. 用户未退出网站A之前，在同一浏览器中，打开一个TAB页访问网站B；
4. 网站B接收到用户请求后，返回一些攻击性代码，并发出一个请求要求访问第三方站点A；
5. 浏览器在接收到这些攻击性代码后，根据网站B的请求，在用户不知情的情况下携带Cookie信息，向网站A发出请求。网站A并不知道该请求其实是由B发起的，所以会根据用户C的Cookie信息以C的权限处理该请求，导致来自网站B的恶意代码被执行。 

举个栗子

​	受害者 Bob 在银行有一笔存款，通过对银行的网站发送请求 http://bank.example/withdraw?account=bob&amount=1000000&for=bob2 可以使 Bob 把 1000000 的存款转到 bob2 的账号下。通常情况下，该请求发送到网站后，服务器会先验证该请求是否来自一个合法的 session，并且该 session 的用户 Bob 已经成功登陆。

​        黑客 Mallory 自己在该银行也有账户，他知道上文中的 URL 可以把钱进行转帐操作。Mallory 可以自己发送一个请求给银行：http://bank.example/withdraw?account=bob&amount=1000000&for=Mallory。但是这个请求来自 Mallory 而非 Bob，他不能通过安全认证，因此该请求不会起作用。

​        这时，Mallory 想到使用 CSRF 的攻击方式，他先自己做一个网站，在网站中放入如下代码： src=”http://bank.example/withdraw?account=bob&amount=1000000&for=Mallory ”，并且通过广告等诱使 Bob 来访问他的网站。当 Bob 访问该网站时，上述 url 就会从 Bob 的浏览器发向银行，而这个请求会附带 Bob 浏览器中的 cookie 一起发向银行服务器。大多数情况下，该请求会失败，因为他要求 Bob 的认证信息。但是，如果 Bob 当时恰巧刚访问他的银行后不久，他的浏览器与银行网站之间的 session 尚未过期，浏览器的 cookie 之中含有 Bob 的认证信息。这时，悲剧发生了，这个 url 请求就会得到响应，钱将从 Bob 的账号转移到 Mallory 的账号，而 Bob 当时毫不知情。等以后 Bob 发现账户钱少了，即使他去银行查询日志，他也只能发现确实有一个来自于他本人的合法请求转移了资金，没有任何被攻击的痕迹。而 Mallory 则可以拿到钱后逍遥法外。 

#### CSRF漏洞如何检测

​	检测CSRF漏洞是一个繁琐的工作，最简单的方法就是抓取一个正常请求的数据包，去掉Referer字段后再重新提交，如果该提交还有效，就说明确定存在有CSRF漏洞

​	现在也有不少黑客工具可以专门针对CSRF漏洞进行检测CSRFTester，CSRF Request Builder等。

​	 以CSRFTester工具为例，CSRF漏洞检测工具的测试原理如下：使用CSRFTester进行检测时，首先抓取我们在浏览器中访问的所有连接以及所有表单等信息，然后通过在CSRFTester中修改相应的表单等信息，重新提交，这就相当于一次伪造客户顿的请求，如果修改后的测试请求成功被网站服务器接受，则说明存在CSRF漏洞。

#### 如何防御CSRF攻击

​	目前防御CSRF攻击主要有三个策略：验证HTTP Referer字段；在请求中加入token并验证；在HTTP头中加入自定义属性并验证。

- 验证 HTTP Referer 字段

  ​这种方法的显而易见的好处就是简单易行，网站的普通开发人员不需要操心 CSRF 的漏洞，只需要在最后给所有安全敏感的请求统一增加一个拦截器来检查 Referer 的值就可以。特别是对于当前现有的系统，不需要改变当前系统的任何已有代码和逻辑，没有风险，非常便捷。

  ​然而，这意味着把安全性都依赖于第三方（也就是浏览器）来实现，因为Referer的值是有浏览器提供的，理论上说并不安全，因为有一些方法可以篡改浏览器赋给请求的 Referer 值

- 在请求地址中添加 token 并验证

  ​**现在业界对CSRF的防御，一致的做法是使用一个Token（Anti CSRF Token）。**

例子：

1. 用户访问某个表单页面。
2. 服务端生成一个Token，放在用户的Session中，或者浏览器的Cookie中。
3. 在页面表单附带上Token参数。
4. 用户提交请求后， 服务端验证表单中的Token是否与用户Session（或Cookies）中的Token一致，一致为合法请求，不是则非法请求。

​       这个Token的值必须是随机的，不可预测的。由于Token的存在，攻击者无法再构造一个带有合法Token的请求实施CSRF攻击。另外使用Token时应注意Token的保密性，尽量把敏感操作由GET改为POST，以form或AJAX形式提交，避免Token泄露。

​        注意：CSRF的Token仅仅用于对抗CSRF攻击。当网站同时存在XSS漏洞时候，那这个方案也是空谈。所以XSS带来的问题，应该使用XSS的防御方案予以解决。

- 在 HTTP 头中自定义属性并验证

​       这种方法也是使用 token 并进行验证，和上一种方法不同的是，这里并不是把 token 以参数的形式置于 HTTP 请求之中，而是把它放到 HTTP 头中自定义的属性里。通过 XMLHttpRequest 这个类，可以一次性给所有该类请求加上 csrftoken 这个 HTTP 头属性，并把 token 值放入其中。这样解决了上种方法在请求中加入 token 的不便，同时，通过 XMLHttpRequest 请求的地址不会被记录到浏览器的地址栏，也不用担心 token 会透过 Referer 泄露到其他网站中去。

​        然而这种方法的局限性非常大。XMLHttpRequest 请求通常用于 Ajax 方法中对于页面局部的异步刷新，并非所有的请求都适合用这个类来发起，而且通过该类请求得到的页面不能被浏览器所记录下，从而进行前进，后退，刷新，收藏等操作，给用户带来不便。另外，对于没有进行 CSRF 防护的遗留系统来说，要采用这种方法来进行防护，要把所有请求都改为 XMLHttpRequest 请求，这样几乎是要重写整个网站，这代价无疑是不能接受的。

        '''
        new_post.tags = random.sample(tag_list, random.randint(1, 3))
        new_post.category_id = catagory_list[random.randint(0, 4)].id

        comment = Comment(id=str(uuid4()), name='tester :' + str(i))
        comment.text = 'comment  Test'
        comment.date = datetime.datetime.now()
        comment.post_id = new_post.id

        db.session.add(new_post)
        db.session.add(comment)

    db.session.commit()


if __name__ == '__main__':
    manager.run()
