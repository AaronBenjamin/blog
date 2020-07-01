from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response
from flask_login import current_user
from sqlalchemy.sql.expression import func
from blog.extensions import db, cache
from blog.models import Post, Tag, Message
from blog.utils import redirect_back
from blog.forms import MessageForm


blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
@blog_bp.route('/index/')
@cache.cached(timeout=360*60, query_string=True)
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/index.html', pagination=pagination, posts=posts)

@blog_bp.route('/about/')
def about():
    return render_template('blog/about.html')

@blog_bp.route('/tag/<int:tag_id>/')
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(tag).order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('blog/tag.html', tag=tag, pagination=pagination, posts=posts)

@blog_bp.route('/post/<slug>/', methods=['GET', 'POST'])
def show_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    form = MessageForm()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Message.query.with_parent(post).order_by(Message.timestamp.asc()).paginate(page, per_page)
    messages = pagination.items
    if form.validate_on_submit():
        title = post.title
        name = form.name.data
        email = form.email.data
        body = form.body.data
        message = Message(title=title, name=name, email=email, body=body, post=post)
        db.session.add(message)
        db.session.commit()
        flash('留言成功！')
        return redirect(url_for('blog.show_post', slug=slug))
    return render_template('blog/post.html', post=post, form=form, pagination=pagination, messages=messages)

@blog_bp.route('/search')
def search():
    per_page = 20
    search_str = request.args.get('search').strip()
    if len(search_str) < 2 or not search_str:
        flash('搜索内容不能少于两个字符', "warning")
        return redirect_back()
    pagination = Post.query.whooshee_search(search_str).paginate(per_page=per_page)
    if pagination.total == 0:
        flash(f'没有搜索到包含{search_str}的结果', 'warning')
        return redirect_back()
    posts = pagination.items
    return render_template('blog/search.html', search_str=search_str, pagination=pagination, posts=posts)
    


