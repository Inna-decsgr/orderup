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
    

# 카테고리 모델(Category)
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

# 음식점 모델 (Restaurant)
class Restaurant(models.Model):
  name = models.CharField(max_length=100)
  address = models.CharField(max_length=255)
  phone_number = models.CharField(max_length=20, null=False)
  rating = models.DecimalField(max_digits=3, decimal_places=1)
  owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
  categories = models.ManyToManyField(Category, related_name='restaurants')
  operating_hours = models.CharField(max_length=100, null=False)
  description = models.TextField()
  image = models.ImageField(upload_to='images/', default='default_image.png')  # 실제 이미지 파일 저장
  image_url = models.URLField(null=False)  # 이미지 URL 저장
  delivery_fee = models.DecimalField(max_digits=7, decimal_places=2)
  menus = models.ManyToManyField('Menu', related_name='restaurants', blank=True)

  def __str__(self):
    return self.name



# 옵션 그룹 모델(OptionGroup)
class OptionGroup(models.Model):
  name = models.CharField(max_length=100)


  def __str__(self):
    return self.name


# 옵션 항목 모델(OptionItem)
class OptionItem(models.Model):
  group = models.ForeignKey(OptionGroup, related_name='options', on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  price = models.DecimalField(max_digits=10, decimal_places=4, default=0)

  def __str__(self):
    return self.name
  
  

# 메뉴 모델(Menu)
class Menu(models.Model):
  restaurant = models.ForeignKey('Restaurant', related_name="menu_items", on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  description = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  available = models.BooleanField(default=True)
  image = models.ImageField(upload_to='menus/', null=True) 
  image_url = models.URLField(null=False, default="")
  quantity = models.PositiveIntegerField(default=1)
  options = models.ManyToManyField(OptionItem, related_name='menus', blank=True)


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