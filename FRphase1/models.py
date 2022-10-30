from django.db import models


class FRdata2(models.Model):
    Username = models.CharField(primary_key=True,max_length=100,default=True)
    img = models.ImageField(upload_to='pics')
    Password = models.IntegerField()





# Create your models here.
