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
import random

ssl._create_default_https_context = ssl._create_unverified_context
tree = ET.parse('deals_computer_5_shops.xml')
root = tree.getroot()
user = User.objects.get(username='kovoli')

shops_list = {'12027': [340, 'Ozon'],
              '42255': [341, 'Ogo1'],
              '72135': [342, '220volt'],
              '75436': [343, 'vseinstrumenti'],
              '74323': [344, 'Ашан']}


def populate_deals():
    offers = root.find('.//offers')
    only_ten = 0
    while True:
        if len(root.findall('.//offer')) == 0:
            break
        try:
            choices_shop = random.choice(list(shops_list.keys()))
            offer = root.find('.//offer/[@merchant_id="{}"]'.format(choices_shop))
            if offer == None:
                continue
            merchand = offer.attrib['merchant_id']
            description = offer.find('description').text
            oldprice = offer.find('oldprice').text
            name = offer.find('name').text
            vendor = offer.find('vendor').text
            price = offer.find('price').text
            url = offer.find('url').text
            regex = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\:)\s"
            subst = "</br>"
            description = re.sub(regex, subst, description, 0, re.MULTILINE)
            param = offer.findall('param')
            parametar = []
            for par in param:
                parametar.append('<li>' + par.attrib['name'] + ': ' + par.text + '</li>')
            parametar = ''.join(parametar)
            original_picture = offer.find('original_picture').text
            input_file = BytesIO(urlopen(original_picture, ).read())

            deal = Deal.objects.create(name=name, vendor=vendor,
                                       price=price, old_price=oldprice,
                                       url=url, categoryId_id=2, description=description,
                                       author=user, shop_id=int(merchand), param=parametar)
            deal.deals_image.save("скидка на" + name + ".jpg", ContentFile(input_file.getvalue()), save=False)
            deal.save()

            offers.remove(offer)
            only_ten += 1
            print('Получилось')
            print(only_ten)
        except Exception as a:
            print(a)
    mydata = ET.tostring(root, encoding="utf-8").decode("utf-8")
    myfile = open("deals_computer_5_shops.xml", "w")
    myfile.write(mydata)
    myfile.close()
    print('Finish!')
    print(len(root.findall('.//offer')))


if __name__ == '__main__':
    populate_deals()
