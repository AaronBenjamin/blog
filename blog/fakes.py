import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from blog import db
from blog.models import Admin, Tag, Post
from blog.utils import slugify

fake = Faker('zh-CN')


def fake_admin():
    admin = Admin(
        username='admin',
        blog_title='赵洪波律师',
        name='赵洪波',
        about='Um, I, Mima Kirigoe, had a fun time as a member of CHAM...'
    )
    admin.set_password('helloflask')
    db.session.add(admin)
    db.session.commit()

def fake_tags(count=10):
    for i in range(count):
        tag = Tag(name=fake.word())
        db.session.add(tag)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            timestamp=fake.date_time_this_year()
        )
        for x in range(random.randint(1,4)):
            tag = Tag.query.get(random.randint(1, Tag.query.count()))
            if tag not in post.tags:
                post.tags.append(tag)
        post.slug = slugify(post.title)
        db.session.add(post)
    db.session.commit()



