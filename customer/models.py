from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'profile'
        verbose_name = ('Profile')
        verbose_name_plural = ('Profile')
        
    def __str__(self):
        return str(self.name)