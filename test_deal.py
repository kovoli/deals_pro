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
tree = ET.parse('deals_first_five_shops.xml')
root = tree.getroot()
user = User.objects.get(username='kovoli')

shops_list = {'12027': [340, 'Ozon'],
              '42255': [341, 'Ogo1'],
              '72135': [342, '220volt'],
              '75436': [343, 'vseinstrumenti'],
              '74323': [344, 'Ашан']}



def populate_deals():
    only_five = 0
    merchant_switch = ''
    offers = root.find('.//offers')
    for offer in root.findall('.//offer'):
        try:
            merchand = offer.attrib['merchant_id']
            if merchant_switch == merchand:
                continue
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
            # categoryId = offer.find('categoryId').text


            deal = Deal.objects.create(name=name, vendor=vendor,
                                       price=price, old_price=oldprice,
                                       url=url, categoryId_id=2, description=description,
                                       author=user, shop_id=shops_list[merchand][0], param=parametar)
            deal.deals_image.save("скидка на" + name + ".jpg", ContentFile(input_file.getvalue()), save=False)
            deal.save()
            merchant_switch = merchand
            offers.remove(offer)
            # 5 добавлений в час
            only_five += 1
            if only_five == 5:
                break
            print('Получилось')
        except Exception as a:
            print(a)
    print('Finish!')


def save_changes_file():
    mydata = ET.tostring(root, encoding="utf-8").decode("utf-8")
    myfile = open("deals_first_five_shops.xml", "w")
    myfile.write(mydata)
    myfile.close()


if __name__ == '__main__':
    populate_deals()
    save_changes_file()
