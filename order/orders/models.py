from django.db import models
from django.contrib.auth.models import User

# 사용자 모델(UserProfile)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_owner = models.BooleanField(default=False)  
    business_registration_number = models.CharField(max_length=50, blank=True, null=True) 

    def __str__(self):
        return self.user.username
  

# 음식점 모델 (Restaurant)
class Restaurant(models.Model):
  name = models.CharField(max_length=100)
  address = models.TextField()
  phone_number = models.CharField(max_length=15)
  rating = models.FloatField(default=0.0)

  def __str__(self):
    return self.name

# 메뉴 모델(Menu)
class Menu(models.Model):
  restaurant = models.ForeignKey(Restaurant, related_name="menus", on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  description = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  available = models.BooleanField(default=True)

  def __str__(self):
    return self.name
  
# 주문 모델 (Order)
class Order(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
  ordered_at = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('delivered', 'Delivered'), ('canceled', 'Canceled')])
  total_price = models.DecimalField(max_digits=10, decimal_places=2)

  def __str__(self):
    return f"Order #{self.id} by {self.user.username}"
  

# 주문 항목 모델 (OrderItem)
class OrderItem(models.Model):
  order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
  menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)

  def __str__(self):
    return f"{self.quantity} x {self.menu.name}"