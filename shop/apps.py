from django.apps import AppConfig
from watson import search as watson

class ShopConfig(AppConfig):
    name = 'shop'
    verbose_name = 'Магазин'

    def ready(self):
        Deal = self.get_model("Deal")
        watson.register(Deal)
