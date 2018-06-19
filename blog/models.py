from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToCover, Resize, ResizeToFit, SmartResize
from ckeditor.fields import RichTextField


# Не обязательно делать
# Post.published.filter(title__startswith='Who') вместо Post.objects.all()
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset() \
            .filter(status='published')


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(User, default=User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(Category, self).save()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:posts_by_category', args=[self.slug])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(User, default=User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(Tag, self).save()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:posts_by_tag', args=[self.slug])

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish', unique=True)
    author = models.ForeignKey(User, default=User,
                               related_name='blog_posts', on_delete=models.CASCADE)
    body = RichTextField(blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='published')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to='post_image/%Y/%m/', blank=True)
    image_detail_blog = ImageSpecField(source='image',
                                       processors=[ResizeToFit(None, 650)],
                                       format='JPEG',
                                       options={'quality': 60})
    image_sidebar_blog = ImageSpecField(source='image',
                                        processors=[ResizeToFit(150, 150)],
                                        format='JPEG',
                                        options={'quality': 60})
    image_list_blog = ImageSpecField(source='image',
                                     processors=[ResizeToFit(None, 348)],
                                     format='JPEG',
                                     options={'quality': 60})

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super(Post, self).save()

    def get_absolute_url(self):
        return reverse('blog:blog_detail',
                       args=[self.slug])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-publish',)
        verbose_name = "Запись"
        verbose_name_plural = 'Записи'


