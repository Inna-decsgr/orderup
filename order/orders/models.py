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
  menu = models.ForeignKey('Menu', related_name='option_groups', on_delete=models.CASCADE, null=True)


  def __str__(self):
    return self.name


# 옵션 항목 모델(OptionItem)
class OptionItem(models.Model):
  group = models.ForeignKey('OptionGroup', related_name='options', on_delete=models.CASCADE)
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
  image = models.ImageField(upload_to='menus/', null=True) 
  image_url = models.URLField(null=False, default="")
  options = models.ManyToManyField('OptionItem', related_name='menus', blank=True)


  def __str__(self):
    return self.name
  


# 주문 모델 (Order)
class Order(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
  ordered_at = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=20, choices=[('pending', '주문 완료'), ('accepted', '주문 수락'), ('delivering', '배달 중'), ('delivered', '배달 완료'), ('canceled', '주문 취소')])
  total_price = models.DecimalField(max_digits=10, decimal_places=2)

  # 결제 정보 추가
  payment_method = models.CharField(max_length=50, blank=True)
  payment_details = models.JSONField(default=dict) # 결제 카드 정보 등을 JSON 형태로 저장
  
  # 리뷰 여부
  review = models.BooleanField(default=False)

  def __str__(self):
    return f"Order #{self.id} by {self.user.username}"
  

# 주문 항목 모델 (OrderItem)
class OrderItem(models.Model):
  order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
  menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)

  def __str__(self):
    return f"{self.quantity} x {self.menu.name}"
  


# OrderItemOption
class OrderItemOption(models.Model):
  order_item = models.ForeignKey(OrderItem, related_name='options', on_delete=models.CASCADE)  # 주문 항목과 연결
  name = models.CharField(max_length=100) 
  price = models.DecimalField(max_digits=10, decimal_places=2)

  def __str__(self):
    return f"{self.name} (+{self.price}원)" 
  


# OrderChart
class OrderChart(models.Model):
  order_id = models.AutoField(primary_key=True)  
  store_id = models.IntegerField()  
  menu_id = models.IntegerField()  
  user_id = models.IntegerField()  
  order_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Order {self.order_id} - Store {self.store_id} - Menu {self.menu_id}"


# Rider
class Rider(models.Model):
  name = models.CharField(max_length=20)
  phone_number = models.CharField(max_length=15)



# Location
class RiderLocation(models.Model):
  rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
  latitude = models.FloatField()
  longitude = models.FloatField()
  timestamp = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=100, choices=[('moving', '이동 중')])

  def __str__(self):
    return f"Rider {self.rider.id} at {self.timestamp}"
  


from django.core.exceptions import ValidationError
# Review
class Review(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
  store = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True) 
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
  image = models.ImageField(upload_to='reviews/', blank=True, null=True) 
  image_url = models.URLField(null=False, default="")
  rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1~5점 제한
  date = models.DateTimeField(auto_now_add=True)
  content = models.TextField(max_length=500)

  def clean(self):
    if not self.image and not self.image_url:
      raise ValidationError("Either an image or an image URL must be provided")


# Like
class Like(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like')
  store = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='like')
  created_at = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.user.username} likes {self.store.name}"