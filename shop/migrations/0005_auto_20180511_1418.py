# Generated by Django 2.0.5 on 2018-05-11 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_coupon_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='CouponType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Тип купона',
                'verbose_name_plural': 'Тип купонов',
            },
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='active',
        ),
        migrations.AlterField(
            model_name='coupon',
            name='promocode',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]