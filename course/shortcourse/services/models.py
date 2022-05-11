from datetime import date
from secrets import choice
from sqlite3 import Date
from turtle import update

from django.db import models
from ckeditor.fields import RichTextField
from django.forms import DateField
from djmoney.models.fields import MoneyField
# from tinymce.model import HTMLField

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager,BaseUserManager

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):

    username=None

    email = models.EmailField(('Email Address'),unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    cnic=models.CharField(max_length=50,)
    contact=models.CharField(max_length=20,blank=True)
    educational_background=models.CharField(max_length=50)
    objects = UserManager()

 
class Course (models.Model):
    course_name= models.CharField(max_length=70,unique=True)
    description=RichTextField()
    price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
        null=True,
        blank=True
    )
 
    course_outline= RichTextField()
    course_image= models.ImageField(upload_to='images')

    def __str__(self):
        return f"{self.course_name}"


class Section (models.Model):

    course= models.ForeignKey(Course,on_delete=models.CASCADE)
    section_title= models.CharField(max_length=70)
    section_start_date= models.DateField()
    section_end_date = models.DateField()  




    def __str__(self):
        return f"{self.course},{self.section_title}"
    
    class Meta:
            unique_together = ('course', 'section_title')

class Enrollment(models.Model):
    choicestatus=(
        ('True','Active'),
        ('False','InActive')
    )
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    section= models.ForeignKey(Section,on_delete=models.CASCADE)
    apply_date= models.DateField()
    activation_Date = models.DateField()

    status = models.CharField(max_length=50,choices=choicestatus)    

    def __str__(self):
        return f"{self.user},{self.section}"


class Review(models.Model):
    course= models.ForeignKey(Course,on_delete=models.CASCADE)
    reply= models.ForeignKey('self',on_delete=models.CASCADE,null=True, related_name="replies")
    comment = models.TextField(max_length=200)   
    name= models.CharField(max_length=50,blank=True,null=True) 
    pub_date= models.DateField(auto_now=True,auto_now_add=False, null=True)
  
    def __str__(self):
        return f"{self.comment}"
    
   