from django.db import models

# Create your models here.

class Image(models.Model):

  # Here we specify model fields

  image = models.ImageField(upload_to='images/%Y/%m/%d/')
  timestamp = models.DateTimeField(auto_now_add=True)     # auto_now_add automatically fills this field with the date of entry creation
  # we will add more fields in later posts

  # Django is using this method to display an object in the Django admin site
  # and as the value inserted into a template when it displays an object
  def __str__(self):
  	return self.image
