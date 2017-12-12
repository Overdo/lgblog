from lgblog import db
from flask import render_template, redirect, flash
from lgblog.models import *
from sqlalchemy import func
from lgblog.forms import CommentForm, PostForm
from os import path
from flask import render_template, Blueprint, redirect, url_for, request
from datetime import datetime
from uuid import uuid4
from flask_login import login_required, current_user
from lgblog.extensions import poster_permission, admin_permission, cache
from flask_principal import Permission, UserNeed, RoleNeed, abort

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

    # Get the tags and sort by count of posts.
    top_tags = db.session.query(
        Tag, func.count(posts_tags.c.post_id).label('total')
    ).join(
        posts_tags
    ).group_by(Tag).order_by('total DESC').limit(5).all()
    return recent, top_tags


@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
@cache.cached(timeout=60)
def blog_list(page=1):
    """View function for home page"""

    posts = Post.query.order_by(
        Post.publish_date.desc()
    ).paginate(page, 5)

    recent, top_tags = sidebar_data()
    return render_template('blog/blog.html',
                           posts=posts,
                           recent=recent,
                           top_tags=top_tags)


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
    recent, top_tags = sidebar_data()

    return render_template('blog/blog_detail.html',
                           post=post,
                           tags=tags,
                           comments=comments,
                           form=form,
                           recent=recent,
                           top_tags=top_tags)


@blog_blueprint.route('/tag/<string:tag_name>')
@cache.cached(timeout=7200, key_prefix='tag_data')
def tag(tag_name):
    """View function for tag page"""

    tag = db.session.query(Tag).filter_by(name=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('blog/blog.html',
                           tag=tag,
                           posts=posts,
                           recent=recent,
                           top_tags=top_tags)


@blog_blueprint.route('/user/<string:username>')
def user(username):
    """View function for user page"""
    user = db.session.query(User).filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('blog/user.html',
                           user=user,
                           posts=posts,
                           recent=recent,
                           top_tags=top_tags)


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
