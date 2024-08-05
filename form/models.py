from django.db import models
from django.utils.translation import gettext_lazy as _


class Registration(models.Model):
    name = models.CharField(max_length=50, null=False)
    created = models.DateTimeField(auto_now_add=True)
    student_no=models.IntegerField(unique=True, null=False)
    branch = models.CharField(max_length=10,null=False)
    section = models.IntegerField(null = False )
    email=models.EmailField(max_length=40, null=False, unique=True )
    phone_number =models.IntegerField(null=False)
    hackerRank_username=models.CharField(max_length=100,null=False)

    class Meta:
        verbose_name_plural = "Registered User"

    def __str__(self):
        return f"{self.name}'s student no is : {self.student_no}"