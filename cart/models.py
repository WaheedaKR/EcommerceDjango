from django.db import models
from shop.models import item, Variation
from admins.models import Account


# Create your models here.

class Cart(models.Model):
    id_cart = models.CharField(max_length=250, blank=True)
    date_of_cart_added = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.id


class ItemCart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(item, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    cart_quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)


    def sub_total(self):
        return self.item.cost * self.cart_quantity

    def __unicode__(self):
        return self.item

    # def __unicode__(self):
    #     return self.product
