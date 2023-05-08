from django.db import models
from categories.models import Categories
from django.urls import reverse
# from accounts.models import Account
# from django.db.models import Avg, Count

# Create your models here.

class item(models.Model):
    name_item    = models.CharField(max_length=200, unique=True)
    url_item            = models.SlugField(max_length=200, unique=True)
    description_item     = models.TextField(max_length=500, blank=True)
    cost           = models.IntegerField()
    picture          = models.ImageField(upload_to='pictures/items')
    stock_item           = models.IntegerField()
    availability    = models.BooleanField(default=True)
    categories        = models.ForeignKey(Categories, on_delete=models.CASCADE)
    date_of_item_created    = models.DateTimeField(auto_now_add=True)
    date_of_item_modified   = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('item_detail', args=[self.categories.url_category, self.url_item])

    def __str__(self):
        return self.name_item

#     def averageReview(self):
#         reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
#         avg = 0
#         if reviews['average'] is not None:
#             avg = float(reviews['average'])
#         return avg
#
#     def countReview(self):
#         reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
#         count = 0
#         if reviews['count'] is not None:
#             count = int(reviews['count'])
#         return count
#
# class VariationManager(models.Manager):
#     def colors(self):
#         return super(VariationManager, self).filter(variation_category='color', is_active=True)
#
#     def sizes(self):
#         return super(VariationManager, self).filter(variation_category='size', is_active=True)
#
# variation_category_choice = (
#     ('color', 'color'),
#     ('size', 'size'),
# )
#
# class Variation(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     variation_category = models.CharField(max_length=100, choices=variation_category_choice)
#     variation_value     = models.CharField(max_length=100)
#     is_active           = models.BooleanField(default=True)
#     created_date        = models.DateTimeField(auto_now=True)
#
#     objects = VariationManager()
#
#     def __str__(self):
#         return self.variation_value
#
#
# class ReviewRating(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(Account, on_delete=models.CASCADE)
#     subject = models.CharField(max_length=100, blank=True)
#     review = models.TextField(max_length=500, blank=True)
#     rating = models.FloatField()
#     ip = models.CharField(max_length=20, blank=True)
#     status = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.subject
