import os
from datetime import date


from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory
from flask_login import login_required, current_user
from flask_ckeditor import upload_success, upload_fail

from blog.extensions import db, cache
from blog.forms import SettingForm, PostForm
from blog.models import Post, Tag
from blog.utils import redirect_back, allowed_file, slugify

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/settings/', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.blog_title = form.blog_title.data
        current_user.phone = form.phone.data
        current_user.weixin = form.weixin.data
        current_user.about = form.about.data
        db.session.commit()
        cache.clear()
        flash('本地缓存已全部清除','success')
        flash('设置更改成功', 'success')
        return redirect(url_for('blog.index'))
    form.blog_title.data = current_user.blog_title
    form.phone.data = current_user.phone
    form.weixin.data = current_user.weixin
    form.about.data = current_user.about
    return render_template('admin/settings.html', form=form)


@admin_bp.route('/post/manage/')
@login_required
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['BLOG_MANAGE_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/manage_post.html', page=page, pagination=pagination, posts=posts)


@admin_bp.route('/post/new/', methods=['GET', 'POST'])
@login_required
def new_post():
    postform = PostForm()
    if postform.validate_on_submit():
        title = postform.title.data
        body = postform.body.data
        if Post.query.filter_by(title=title).first():
            slug =slugify(title+date.isoformat(date.today()))
        else:
            slug=slugify(title)
        post = Post(title=title, body=body, slug=slug)
        for name in postform.tag.data.split():
            tag = Tag.query.filter_by(name=name).first()
            if tag is None:
                tag = Tag(name=name)
                db.session.add(tag)
                db.session.commit()
            if tag not in post.tags:
                post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
        cache.clear()
        flash('本地缓存已全部清除', 'success')
        flash('发表成功！', 'success')
        return redirect(url_for('blog.show_post', slug=slug))
    return render_template('admin/new_post.html', postform=postform)


@admin_bp.route('/post/edit/<slug>/', methods=['GET', 'POST'])
@login_required
def edit_post(slug):
    postform = PostForm()
    post = Post.query.filter_by(slug=slug).first_or_404()
    if postform.validate_on_submit():
        if post.title == postform.title.data:
            post.slug = post.slug
        elif Post.query.filter_by(title=postform.title.data).first():
            post.slug = slugify(postform.title.data+date.isoformat(date.today()))
        else:
            post.slug = slugify(postform.title.data)
        post.title = postform.title.data
        post.body = postform.body.data 
        for name in postform.tag.data.split():
            tag = Tag.query.filter_by(name=name).first()
            if tag is None:
                tag = Tag(name=name)
                db.session.add(tag)
                db.session.commit()
            if tag not in post.tags:
                post.tags.append(tag)
                db.session.commit()
        db.session.add(post)
        db.session.commit()
        cache.clear()
        flash('本地缓存已全部清除', 'success')
        flash('文章修改成功！', 'success')
        return redirect(url_for('blog.show_post', slug=post.slug))
    postform.title.data = post.title
    postform.tag.data = ' '.join([tag.name for tag in post.tags])
    postform.body.data = post.body
    return render_template('admin/edit_post.html', post=post, postform=postform)


@admin_bp.route('/post/delete/<slug>/', methods=['POST'])
@login_required
def delete_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    db.session.delete(post)
    db.session.commit()
    cache.clear()
    flash('本地缓存已全部清除', 'success')
    flash('文章删除成功', 'success')
    return redirect_back()




@admin_bp.route('/manage/tag/')
@login_required
def manage_tag():
    return render_template('admin/manage_tag.html')






@admin_bp.route('/delete/tag/<slug>/<int:tag_id>', methods=['POST'])
@login_required
def delete_tag(slug, tag_id):
    tag = Tag.query.get_or_404(tag_id)
    post = Post.query.filter_by(slug).first_or_404()
    post.tags.remove(tag)
    db.session.commit()
    cache.clear()
    flash('本地缓存已全部清除', 'success')
    
    if not tag.photos:
        db.session.delete(tag)
        db.session.commit()

    flash('标签删除成功', 'info')
    return redirect(url_for('.show_post', slug=slug))


@admin_bp.route('/delete/tag/<int:tag_id>', methods=['POST'])
@login_required
def delete_tags(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    cache.clear()
    flash('本地缓存已全部清除', 'success')
    flash('标签删除成功', 'info')
    return redirect(url_for('.manage_tag'))




@admin_bp.route('/uploads/<path:filename>/')
def get_image(filename):
    return send_from_directory(current_app.config['BLOG_UPLOAD_PATH'], filename)



@admin_bp.route('/upload/', methods=['POST'])
def upload_image():
    f = request.files.get('upload')
    if not allowed_file(f.filename):
        return upload_fail('只允许上传图片')
    f.save(os.path.join(current_app.config['BLOG_UPLOAD_PATH'], f.filename))
    url = url_for('.get_image', filename=f.filename)
    return upload_success(url, f.filename)

