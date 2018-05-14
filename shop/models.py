from django.db import models
from django.utils import timezone
from unidecode import unidecode
from django.template.defaultfilters import slugify
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import Resize, ResizeCanvas, ResizeToCover, ResizeToFill, ResizeToFit, SmartResize
from django.contrib.auth.models import User


class Store(models.Model):
    title = models.CharField(max_length=100, verbose_name='магазин', unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='store_image/%Y/%m/', blank=True)
    image_store = ImageSpecField(source='image',
                                 processors=[Resize(200, 200)],
                                 format='JPEG',
                                 options={'quality': 50})
    img_single_store = ImageSpecField(source='image',
                                      processors=[Resize(200, 100)],
                                      format='JPEG',
                                      options={'quality': 50})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super(Store, self).save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:store_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(Category, self).save()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('deal:deals_by_category', args=[self.slug])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class CouponType(models.Model):
    type = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.type))
        super(CouponType, self).save()

    def __str__(self):
        return self.type


    class Meta:
        verbose_name = 'Тип купона'
        verbose_name_plural = 'Тип купонов'


class Coupon(models.Model):
    title = models.CharField(max_length=250, verbose_name='Купон')
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, default=User,
                               related_name='shop_coupons', on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    shop = models.ForeignKey(Store, on_delete=models.CASCADE)
    coupon_link = models.URLField(max_length=250)
    expired = models.DateTimeField()
    promocode = models.CharField(max_length=200, blank=True)
    coupon_type = models.ForeignKey(CouponType, related_name='Тип_купона', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='coupon_image/%Y/%m', blank=True)
    coupon_image = ImageSpecField(source='image',
                                 processors=[Resize(600, 400)],
                                 format='JPEG',
                                 options={'quality': 50})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super(Coupon, self).save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('coupon:coupon_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'


class Deal(models.Model):
    name = models.CharField(max_length=250, verbose_name='скидка')
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, default=User, on_delete=models.CASCADE)
    description = models.TextField()
    vendor = models.CharField(max_length=200)
    shop = models.ForeignKey(Store, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.URLField()
    categoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
    original_picture = models.ImageField(upload_to='deals_images/%Y/%m', blank=True)
    deals_image = ImageSpecField(source='original_picture',
                                  processors=[ResizeCanvas(753, 700)],
                                  format='JPEG',
                                  options={'quality': 70})
    deals_grid_image = ImageSpecField(source='original_picture',
                                 processors=[ResizeCanvas(753, 700)],
                                 format='JPEG',
                                 options={'quality': 50})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(Deal, self).save()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('deal:deal_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'
