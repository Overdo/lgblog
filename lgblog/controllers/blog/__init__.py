from lgblog import db
from flask import render_template, redirect, flash
from lgblog.models import *
from sqlalchemy import func, or_
from lgblog.forms import CommentForm, PostForm, SearchForm
from os import path
from flask import render_template, Blueprint, redirect, url_for, request
from datetime import datetime
from uuid import uuid4
from flask_login import login_required, current_user
from lgblog.extensions import poster_permission, admin_permission, cache
from flask_principal import Permission, UserNeed, RoleNeed, abort
import logging

logging.basicConfig(level=logging.INFO)

blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder=path.join('templates/blog'),
    url_prefix='/blog')


@cache.cached(timeout=7200, key_prefix='sidebar_data')
def sidebar_data():
    """Set the sidebar function."""

    # Get post of recent
    recent = db.session.query(Post).order_by(
        Post.publish_date.desc()
    ).limit(5).all()

    all_tags = Tag.query.order_by(Tag.id).all()

    categories = Category.query.order_by(Category.id).all()
    return recent, all_tags, categories


@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
@blog_blueprint.route('/tag/<string:tag_name>/<int:page>')
@blog_blueprint.route('/tag/<string:tag_name>')
@blog_blueprint.route('/category/<string:category_name>/<int:page>')
@blog_blueprint.route('/category/<string:category_name>')
@blog_blueprint.route('/search/<string:search_string>/<int:page>')
@cache.cached(timeout=60)
def blog_list(page=1, tag_name=None, category_name=None, search_string=None):
    """View function for home page"""
    form = SearchForm()
    logging.info(search_string)

    if search_string:
        posts = Post.query.filter(or_(Post.title.contains(search_string), Post.text.contains(search_string))) \
            .order_by(Post.publish_date.desc()).paginate(page, 5)
        recent, all_tags, categories = sidebar_data()
        return render_template('blog/blog_list.html',
                               posts=posts,
                               search_string=search_string,
                               category_name=None,
                               form=form,
                               tag_name=None,
                               categories=categories,
                               recent=recent,
                               all_tags=all_tags)
    if category_name:
        category = db.session.query(Category).filter_by(name=category_name).first_or_404()
        posts = category.posts.order_by(Post.publish_date.desc()).paginate(page, 5)
        recent, all_tags, categories = sidebar_data()
        return render_template('blog/blog_list.html',
                               posts=posts,
                               category_name=category_name,
                               tag_name=None,
                               form=form,
                               search_string=None,
                               categories=categories,
                               recent=recent,
                               all_tags=all_tags)
    if tag_name:
        tag = db.session.query(Tag).filter_by(name=tag_name).first_or_404()
        posts = tag.posts.order_by(Post.publish_date.desc()).paginate(page, 5)
        recent, all_tags, categories = sidebar_data()
        return render_template('blog/blog_list.html',
                               posts=posts,
                               category_name=None,
                               search_string=None,
                               form=form,
                               categories=categories,
                               tag_name=tag_name,
                               recent=recent,
                               all_tags=all_tags)
    posts = Post.query.order_by(
        Post.publish_date.desc()
    ).paginate(page, 5)
    recent, all_tags, categories = sidebar_data()
    return render_template('blog/blog_list.html',
                           posts=posts,
                           category_name=None,
                           tag_name=None,
                           form=form,
                           search_string=None,
                           categories=categories,
                           all_tags=all_tags,
                           recent=recent)


@blog_blueprint.route('/search/<int:page>', methods=('GET', 'POST'))
def search_blog(page=1):
    form = SearchForm()
    recent, all_tags, categories = sidebar_data()

    if request.form['search_string'] and request.method == 'POST':

        search_string = request.form['search_string']
        posts = Post.query.filter(or_(Post.title.contains(search_string), Post.text.contains(search_string))) \
            .order_by(Post.publish_date.desc())
        if len(posts.all()) < 1:
            posts = Post.query.order_by(
                Post.publish_date.desc()
            ).paginate(page, 5)
            return render_template('blog/blog_404.html',
                                   posts=posts,
                                   category_name=None,
                                   tag_name=None,
                                   form=form,
                                   search_string=None,
                                   categories=categories,
                                   all_tags=all_tags,
                                   recent=recent)
        else:
            return render_template('blog/blog_list.html',
                                   posts=posts.paginate(page, 5),
                                   form=form,
                                   search_string=search_string,
                                   category_name=None,
                                   tag_name=None,
                                   categories=categories,
                                   recent=recent,
                                   all_tags=all_tags)
    else:

        posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, 5)
        return render_template('blog/blog_list.html',
                               posts=posts,
                               category_name=None,
                               tag_name=None,
                               form=form,
                               search_string=None,
                               categories=categories,
                               all_tags=all_tags,
                               recent=recent)


def make_cache_key(*args, **kwargs):
    """Dynamic creation the request url."""

    path = request.path
    args = str(hash(frozenset(request.args.items())))
    # lang = get_locale()
    # return (path + args + lang).encode('utf-8')
    return (path + args).encode('utf-8')


@blog_blueprint.route('/post/<string:post_id>', methods=('GET', 'POST'))
@cache.cached(timeout=60, key_prefix=make_cache_key)
def blog_detail(post_id):
    """View function for post page"""

    form = CommentForm()
    # form.validate_on_submit() will be true and return the
    # data object to form instance from user enter,
    # when the HTTP request is POST
    if form.validate_on_submit():
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        new_comment.date = datetime.now()
        new_comment.post_id = post_id
        db.session.add(new_comment)
        db.session.commit()

    post = db.session.query(Post).get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, all_tags, categories = sidebar_data()

    return render_template('blog/blog_detail.html',
                           post=post,
                           tags=tags,
                           categories=categories,
                           comments=comments,
                           all_tags=all_tags,
                           form=form,
                           recent=recent)


@blog_blueprint.route('/tag/<string:tag_name>/')
@cache.cached(timeout=7200)
def tag(tag_name, page=1):
    """View function for tag page"""
    form = SearchForm()
    tag = db.session.query(Tag).filter_by(name=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).paginate(page, 5)
    recent, all_tags, categories = sidebar_data()

    return render_template('blog/blog_list.html',
                           tag=tag,
                           posts=posts,
                           form=form,
                           categories=categories,
                           all_tags=all_tags,
                           recent=recent,
                           tag_name=tag_name)


@blog_blueprint.route('/user/<string:username>')
def user(username):
    """View function for user page"""
    user = db.session.query(User).filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, all_tags, categories = sidebar_data()

    return render_template('blog/user.html',
                           user=user,
                           posts=posts,
                           recent=recent,
                           all_tags=all_tags)


@blog_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    """View function for new_port."""
    form = PostForm()

    if not current_user:
        flash("you need login!!!")
        return redirect(url_for('blog.blog_list'))

    if form.validate_on_submit():
        new_post = Post(id=str(uuid4()), title=form.title.data)
        new_post.text = form.text.data
        new_post.publish_date = datetime.now()
        new_post.user_id = current_user.get_id()
        role = db.session.query(Role).filter_by(name='poster').first()
        role.users.append(current_user)
        db.session.add(new_post)
        db.session.add(role)
        db.session.commit()
        return redirect(url_for('blog.blog_list'))

    return render_template('blog/new_post.html',
                           form=form)


@blog_blueprint.route('/edit/<string:id>', methods=['GET', 'POST'])
@login_required
@poster_permission.require(http_exception=403)
def edit_post(id):
    """View function for edit_post."""

    post = Post.query.get_or_404(id)

    # Ensure the user logged in.
    if not current_user:
        flash("you need login")
        return redirect(url_for('main.login'))

    #
    # # Only the post onwer can be edit this post.
    # if current_user != post.users:
    #     flash('Only the post onwer can be edit this post.')
    #     return redirect(url_for('blog.blog_detail', post_id=id))

    # 当 user 是 poster 或者 admin 时, 才能够编辑文章
    # Admin can be edit the post.
    permission = Permission(UserNeed(post.users.id))
    if permission.can() or admin_permission.can():
        form = PostForm()

        if form.validate_on_submit():
            post.title = form.title.data
            post.text = form.text.data
            post.publish_date = datetime.now()

            # Update the post
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.blog_detail', post_id=post.id))
    else:
        abort(403)

    form.title.data = post.title
    form.text.data = post.text
    return render_template('blog/edit_post.html', form=form, post=post)
