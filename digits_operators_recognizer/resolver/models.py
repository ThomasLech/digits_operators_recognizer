from django.db import models

# Create your models here.

class Image(models.Model):

    # Here we specify model fields
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    # auto_now_add set to true makes this field filled with the date of entry creation
    timestamp = models.DateTimeField(auto_now_add=True)
    # we will add more fields here later

    # Django is using this method to display an object in the Django admin site
    def __str__(self):
        return self.image
