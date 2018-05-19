from django.apps import AppConfig
from watson import search as watson


class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = 'Блог'

    def ready(self):
        Post = self.get_model("Post")
        watson.register(Post)
