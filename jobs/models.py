from django.db import models

# Create your models here.
class JobsDb(models.Model):
    employer = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description	= models.TextField()
    CATEGORY_CHOICES = (
        ("software", "Software Development"),
        ("data", "Data & Analytics"),
        ("design", "Design"),
        ("marketing", "Marketing"),
        ("sales", "Sales"),
        ("finance", "Finance & Accounting"),
        ("hr", "Human Resources"),
        ("support", "Customer Support"),
        ("other", "Other"),
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="software")
    EXPERIENCE_CHOICES = (
        ("fresher", "Fresher"),
        ("mid", "Mid"),
        ("senior", "Senior"),
    )  
    experience_level = models.CharField(max_length=20, choices= EXPERIENCE_CHOICES, default="fresher")
    location = models.CharField(max_length=50)
    posted_date	= models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField(default=True)