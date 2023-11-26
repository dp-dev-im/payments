from dataclasses import dataclass

import requests
from django.core.files.base import ContentFile
from django.core.management import BaseCommand
from tqdm import tqdm

from mall.models import Category, Product

BASE_URL = "https://raw.githubusercontent.com/dp-dev-im/payments/main/mall/data/"


@dataclass
class Item:
    category_name: str
    name: str
    price: int
    priceUnit: str
    desc: str
    photo_path: str


class Command(BaseCommand):
    help = "Load product from JSON file"

    def handle(self, *args, **options):
        json_url = BASE_URL + "product-list.json"
        item_dict_list = requests.get(json_url).json()

        item_list = [Item(**item_dict) for item_dict in item_dict_list]
        # print(item_list)

        category_name_set = {item.category_name for item in item_list}
        # print(category_name_set)

        category_dict = {}
        for category_name in category_name_set:
            category, __ = Category.objects.get_or_create(
                name=category_name or "undefined"
            )
            category_dict[category.name] = category

        for item in tqdm(item_list):
            category: Category = category_dict[item.category_name or "undefined"]
            product, is_created = Product.objects.get_or_create(
                category=category,
                name=item.name,
                defaults={
                    "description": item.desc,
                    "price": item.price,
                },
            )

            if is_created:
                photo_url = BASE_URL + item.photo_path
                filename = photo_url.rsplit("/", 1)[-1]
                photo_data = requests.get(photo_url).content
                product.photo.save(
                    name=filename, content=ContentFile(photo_data), save=True
                )
