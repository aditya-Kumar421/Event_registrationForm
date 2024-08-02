from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

def validate_akgec_email(value):
        if not value.endswith('@akgec.ac.in'):
            raise ValidationError(
                _('Only college email id is allowed.'),
                params={'value': value},
            )

def validate_Phone_digits(value):
    min_digits = 10  
    max_digits = 10  
    value_str = str(value)
    if len(value_str) < min_digits or len(value_str) > max_digits:
        raise ValidationError(
            f"Contact number must have 10 digits."
        )
def validate_Student_digits(value):
    min_digits = 7  
    max_digits = 8  
    value_str = str(value)
    if len(value_str) < min_digits or len(value_str) > max_digits:
        raise ValidationError(
            f"Student number must have 7 or 8 digits."
        )
def validate_Section_digits(value):
    min_digits = 1
    max_digits = 20 
    if value < min_digits or value > max_digits:
        raise ValidationError(
            f"Section must be between 1 to 20."
        )
class Registration(models.Model):
    name = models.CharField(max_length=50, null=False)
    created = models.DateTimeField(auto_now_add=True)
    student_no=models.IntegerField(validators=[MinValueValidator(2200000),MaxValueValidator(23999999),validate_Student_digits],unique=True, null=False)
    branch = models.CharField(max_length=10,null=False)
    section = models.IntegerField(default=1,null = False,validators=[MinValueValidator(1),MaxValueValidator(20),validate_Section_digits] )
    email=models.EmailField(max_length=40,validators=[validate_akgec_email], null=False, unique=True )
    phone_number =models.IntegerField(validators=[MinValueValidator(1000000000),MaxValueValidator(9999999999), validate_Phone_digits], null=False)
    hackerRank_username=models.CharField(max_length=100,null=True)

    class Meta:
        verbose_name_plural = "Registered User"

    def __str__(self):
        return f"{self.name}'s student no is : {self.student_no}"