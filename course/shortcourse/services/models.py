from django.db import models
from ckeditor.fields import RichTextField
from djmoney.models.fields import MoneyField
from django.db.models.signals import pre_save
from datetime import date

from .utils import generate_section_slug, generate_course_slug

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

    cnic = models.CharField(max_length=16, blank=True, null=True)
    contact=models.CharField(max_length=20,blank=True)
    educational_background = models.TextField(null = False)
    image= models.ImageField(upload_to='images/users', default="avatar.png")

    objects = UserManager()



class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
         verbose_name = "Category"
         verbose_name_plural = "Categories"

class FAQ(models.Model):
    question = models.CharField(max_length=100, null=False)
    answer = models.TextField(null=False)
    
    def __str__(self):
        return f"{self.question}"

class Assignment(models.Model):
    name = models.CharField(max_length=100)
    due_date = models.DateField(null=True)
    file = models.FileField(upload_to='assignments', null = False)


    def __str__(self):
        return f"{self.name}"
    
class Course (models.Model):
    courseLevelChoice=(
        ('Beginner','Beginner'),
        ('Intermediate','Intermediate'),
        ('Exert', 'Expert'))
    course_name= models.CharField(max_length=70,unique=True)
    description=RichTextField()
    price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='PKR',
        max_digits=11,
        null=True,
        blank=True
    )
    course_level = models.CharField(max_length=20, choices = courseLevelChoice, null=False, default="Beginner")
    total_enrollments = models.IntegerField(default=0, null=False, blank= False)
    course_outline= RichTextField()
    course_image= models.ImageField(upload_to='images/courses')
    instructors  = models.ManyToManyField(User)
    Faqs  = models.ManyToManyField(FAQ)
    slug = models.SlugField(unique=True, blank=True, null=True)
    seo_title = models.CharField(max_length=40, null=True)
    seo_keywords = models.TextField(max_length=100, null=True)
    seo_description = models.TextField(null=True)
    
    def __str__(self):
        return f"{self.course_name}"

    
def course_slug_generator(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug= generate_course_slug(instance)

pre_save.connect(course_slug_generator,sender= Course)


class Section (models.Model):
    status_choices = (('OPEN' , 'OPEN'), ('IN PROGRESS', 'IN PROGRESS'), ('CLOSED', 'CLOSED'), ('UPCOMING', 'UPCOMING'))
    course= models.ForeignKey(Course,on_delete=models.CASCADE, related_name = "sections")
    section_title= models.CharField(max_length=70)
    section_start_date= models.DateField()
    section_end_date = models.DateField() 
    enrollment_start_date = models.DateField(null=True)
    enrollment_end_date = models.DateField(null=True, blank= True) 
    section_status = models.CharField(max_length=20, null = False, default='OPEN', choices=status_choices)
    assignments = models.ManyToManyField(Assignment, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    

    def __str__(self):
        return f"{self.course},{self.section_title}"    
    class Meta:
            unique_together = ('course', 'section_title')

def slug_generator(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = generate_section_slug(instance)

pre_save.connect(slug_generator,sender= Section)

class Enrollment(models.Model):
    choicestatus=(
        ('In Review','In Review'),
        ('Approved','Approved'),
        ('In Progress','In Progress'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    section= models.ForeignKey(Section,on_delete=models.CASCADE)
    apply_date= models.DateField(default=date.today())
    activation_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50,choices=choicestatus, default="In Review")
    comment=models.CharField(max_length=200,null=True, blank=True)    

    def __str__(self):
        return f"{self.user}-{self.section}"

    class Meta:
        unique_together = ['user', 'section']


def increment_enrollments(sender,instance,*args,**kwargs):
    c = Course.objects.get(id = instance.section.course_id)
    c.total_enrollments = c.total_enrollments + 1
    c.save()

pre_save.connect(increment_enrollments,sender= Enrollment)


class Review(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE, related_name="reviews")
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True, related_name="replies")
    comment = models.TextField(max_length=200)   
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    pub_date = models.DateField(auto_now=True,auto_now_add=False, null=True)
   
   
    def __str__(self):
        return f"{self.comment}"

class Service(models.Model):
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    title =  models.CharField(max_length=40,  null=False)
    description = models.TextField(null=False)
    image= models.ImageField(upload_to='images/services', null = True)
    
    def __str__(self):
        return f"{self.title}"
    

class Project(models.Model):
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    name  = models.CharField(max_length=60)
    person_name = models.CharField(max_length=60)
    charges = models.DecimalField(max_digits=15, decimal_places=2)
    start_date = models.DateField(blank=True, null=True)
    site_link = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"



    