import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'deals_pro.settings')

import django

django.setup()
from shop.models import Store


def populate():
    for i in range(1, 600):
        post = Store.objects.create(title='Магазин ' + str(i), content='Post body. ' * 15 + str(i))
        post.save()

    print('Finish!')


if __name__ == '__main__':
    populate()