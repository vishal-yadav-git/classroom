from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import datetime
from django.conf import settings
from PIL import Image

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

USER_TYPE_CHOICES = (
    ('student','Student'),
    ('faculty','Faculty'),
    ('admin','Admin'),
)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=50, null=True, blank=True)
    occupation = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='profile_pics/', default='img/user.jpg', blank=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone', 'user_type']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Course(models.Model):
    name = models.CharField(max_length=100)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name
 

class Faculty(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    institute = models.CharField(max_length=50, null=False, blank=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    show_on_homepage = models.BooleanField(default=False) 

    def __str__(self):
        return self.name
    
class FacultyComment(models.Model):
    name = models.CharField(max_length=100)  # Instead of linking to a user
    content = models.TextField()
    post = models.ForeignKey(Faculty, related_name="faculty_comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='faculty_replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} on {self.post}"


class Lecture(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    title = models.CharField(max_length=50, null=False, blank=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=300, null=False, blank=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pub_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    show_on_homepage = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.email} - {self.course.name}"

    def total_price(self):
        return self.course.price * self.quantity
    

class Comment(models.Model):
    name = models.CharField(max_length=100)  # Instead of linking to a user
    content = models.TextField()
    post = models.ForeignKey(Lecture, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} on {self.post}"


class Franchisee(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    pub_date = models.DateTimeField(default=datetime.now)
    is_published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
class SlideBanner(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=300, null=False, blank=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    
class Filter(models.Model):
    subject = models.CharField(max_length=100, null=False, blank=False)
    faculty = models.TextField(max_length=300, null=False, blank=False)
    course = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.faculty
    
# added mannully by vishal yadav 
class MyModel(models.Model):
    image = models.ImageField(upload_to='images/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img = img.resize(output_size, Image.ANTIALIAS)
            img.save(self.image.path)