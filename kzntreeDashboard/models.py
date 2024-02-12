# myapp/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserProfileManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    sku = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.CharField(max_length=255, blank=True)
    
    # Merged field for in-stock status and value
    in_stock = models.FloatField()
    
    # Merged field for available stock status and value
    available_stock = models.FloatField()

    def in_stock_status(self):
        # Implement your logic to determine the status based on in_stock value
        if self.in_stock > 10:
            return 'H'  # High
        else:
            return 'L'  # Low

    def available_stock_status(self):
        # Implement your logic to determine the status based on available_stock value
        if self.available_stock > self.in_stock * 0.5:
            return 'H'  # High
        else:
            return 'L'  # Low

    def __str__(self):
        return self.name

class BuildDashboard(models.Model):
    references = models.CharField(max_length=255)
    item_group = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    linked_sale_order_group = models.CharField(max_length=255)
    creation_group_date = models.DateField()
    completion_group_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.references