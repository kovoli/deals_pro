import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'deals_pro.settings')

import django

django.setup()
from shop.models import Deal
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from io import BytesIO
from urllib.request import urlopen
import ssl
import re
import random
import requests, zipfile, io, os
import xml.etree.ElementTree as ET
import sys
from category_list import cat_list


name_cat = sys.argv[1]

categorys_urls_zip = {'computer': 'http://exporter.gdeslon.ru/uploads/exports/2639de456d5f02500bb26aea0ba5810d9ad6b538.xml.zip',
                      'bit_tech': 'http://exporter.gdeslon.ru/uploads/exports/f1f0417997071cef460f9049cae1fbc9d2f72dad.xml.zip',
                      'phones': 'http://exporter.gdeslon.ru/uploads/exports/a360a57b50582994c6d4715371d5e4f3093fe539.xml.zip',
                      'dlja_sada': 'http://exporter.gdeslon.ru/uploads/exports/11ff8a413c41de1ddf16d041462c681aaddba2be.xml.zip'}


r = requests.get(categorys_urls_zip[name_cat])
zipfile = zipfile.ZipFile(io.BytesIO(r.content))
filename = zipfile.namelist()[0]
zipfile.extractall()


tree = ET.parse(filename)
root = tree.getroot()

os.remove(filename)


offers = root.find('.//offers')
offers_complet = 0
offers_delete = 0
for offer in root.findall('.//offer'):
    offers_complet += 1
    description = offer.find('description').text
    oldprice = offer.find('oldprice').text
    if description is None or len(description) < 150 or oldprice is None:
        offers_delete += 1
        offers.remove(offer)
        continue


mydata = ET.tostring(root, encoding='utf-8').decode('utf-8')
myfile = open("{}_imports.xml".format(name_cat), "w")
myfile.write(mydata)
print('Всего:', offers_complet, 'Стер:', offers_delete, 'Осталось:', offers_complet - offers_delete)


ssl._create_default_https_context = ssl._create_unverified_context
tree = ET.parse('{}_imports.xml'.format(name_cat))
root = tree.getroot()
user = User.objects.get(username='kovoli')

shops_list = {'12027': [340, 'Ozon'],
              '42255': [341, 'Ogo1'],
              '72135': [342, '220volt'],
              '75436': [343, 'vseinstrumenti'],
              '74323': [344, 'Ашан']}

offers = root.find('.//offers')
#only_ten = 0
while True:
    if len(root.findall('.//offer')) == 0:
        break
    try:
        choices_shop = random.choice(list(shops_list.keys()))
        offer = root.find('.//offer/[@merchant_id="{}"]'.format(choices_shop))
        if offer == None:
            continue
        merchand = offer.attrib['merchant_id']
        category = offer.attrib['gs_category_id']
        if category not in cat_list[name_cat][0]:
            category = cat_list[name_cat][1][0]
        description = offer.find('description').text
        oldprice = offer.find('oldprice').text
        name = offer.find('name').text
        vendor = offer.find('vendor').text
        #offer_id = offer.attrib['id']
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
                                   url=url, categoryId_id=int(category), description=description,
                                   author=user, shop_id=int(merchand), param=parametar)
        deal.deals_image.save("скидка на" + name + ".jpg", ContentFile(input_file.getvalue()), save=False)
        deal.save()

        offers.remove(offer)
        #only_ten += 1
        print('Получилось')
        #print(only_ten)
    except Exception as a:
        offers.remove(offer)
        print(a)
mydata = ET.tostring(root, encoding="utf-8").decode("utf-8")
myfile = open("{}_imports.xml".format(name_cat), "w")
myfile.write(mydata)
myfile.close()
print('Finish!')
print(len(root.findall('.//offer')))


