from django.db import models
from django.urls import reverse

# Create your models here.

class Categories(models.Model):
    main_category = models.CharField(max_length=50, unique=True)
    url_category = models.SlugField(max_length=100, unique=True)
    description_category = models.TextField(max_length=255, blank=True)
    pic_category = models.ImageField(upload_to='pictures/categories', blank=True)

    class Meta:
        verbose_name = 'categories'
        verbose_name_plural = 'categories'

    def get_url(self):
            return reverse('items_by_categories', args=[self.url_category])

    def __str__(self):
        return self.main_category
