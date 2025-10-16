from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class InventoryItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inventory_items")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class InventoryChange(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='changes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    old_quantity = models.PositiveBigIntegerField()
    new_quantity = models.PositiveBigIntegerField()
    change_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name}: {self.old_quantity} → {self.new_quantity}"