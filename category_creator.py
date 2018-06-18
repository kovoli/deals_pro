import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'deals_pro.settings')

import django

django.setup()
from shop.models import Category

import xml.etree.ElementTree as ET

tree = ET.parse('telephone_categories.xml')
root = tree.getroot()

cat_list = []
for cat in root.iter('category'):
    categ = Category.objects.get(id=4)
    print(cat.attrib['id'])
    cat_list.append(cat.attrib['id'])
    print(cat_list)
    Category.objects.create(id=cat.attrib['id'], name=cat.text, parent=categ)
