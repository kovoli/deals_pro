import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'deals_pro.settings')

import django

django.setup()
from blog.models import Post, Tag
from django.contrib.auth.models import User

user = User.objects.get(username='kovoli')


def populate():
    for i in range(1, 1000):
        post = Post.objects.create(title='Статья ' + str(i), body='Post body. ' * 15 + str(i), author=user, category_id=1)
        post.save()

    print('Finish!')


if __name__ == '__main__':
    populate()