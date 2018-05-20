import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'deals_pro.settings')

import django

django.setup()
from shop.models import Deal
from django.contrib.auth.models import User
import xml.etree.ElementTree as ET
from django.core.files.base import ContentFile
from io import BytesIO
from urllib.request import urlopen
import ssl
import re
ssl._create_default_https_context = ssl._create_unverified_context
tree = ET.parse('test.xml')

user = User.objects.get(username='kovoli')
root = tree.getroot()


def populate_deals():
    for offer in root.findall('.//offer'):
        try:
            description = offer.find('description').text
            if description == None and len(description) < 150:
                continue
            oldprice = offer.find('oldprice').text
            if oldprice == None:
                continue
            name = offer.find('name').text
            vendor = offer.find('vendor').text
            price = offer.find('price').text
            url = offer.find('url').text
            regex = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\:)\s"
            subst = "</br>"
            description = re.sub(regex, subst, description, 0, re.MULTILINE)
            original_picture = offer.find('original_picture').text
            input_file = BytesIO(urlopen(original_picture, ).read())
            # categoryId = offer.find('categoryId').text
            deal = Deal.objects.create(name=name, vendor=vendor,
                                       price=price, old_price=oldprice,
                                       url=url, categoryId_id=1, description=description, author=user, shop_id=241)
            deal.original_picture.save("скидка на" + name + ".jpg", ContentFile(input_file.getvalue()), save=False)
            deal.save()
            print('Получилось')
        except Exception as a:
            print(a)
    print('Finish!')


if __name__ == '__main__':
    populate_deals()

