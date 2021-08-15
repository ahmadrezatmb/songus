from django.db import models

class temperoryaccount(models.Model):
    username = models.CharField(max_length=256 , null=True , blank=True)
    password = models.CharField(max_length=256 , null=True , blank=True)
    email = models.CharField(max_length=256 , null=True , blank=True)
    code = models.CharField(max_length=50 , null=True , blank=True)
    isactivenow = models.BooleanField(default=False , null= True , blank=True)

    def __str__(self):
        return str(self.username) + ' with email ' + str(self.email)