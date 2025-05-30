from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, name=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, name=None):
        user = self.create_user(email=email, password=password, name=name)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    inr_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.email} Wallet"
    
class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    sender_ip = models.GenericIPAddressField()
    
    def __str__(self):
        return f"{self.sender.email} sent ₹{self.amount} to {self.receiver.email}"