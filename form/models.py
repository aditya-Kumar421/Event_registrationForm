from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

#from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
def validate_akgec_email(value):
        if not value.endswith('@akgec.ac.in'):
            raise ValidationError(
                _('Only emails with @akgec.ac.in domain are allowed.'),
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
# phone_regex = RegexValidator(
#     regex=r'^\+?91?\d{10,14}$',
#     message="Phone number must be entered in the format: '+910123456789'. Up to 13 digits allowed."
# )
class Registration(models.Model):
    MALE = 'Male'
    FEMALE= 'Female'
    OTHER = 'Other'

    Hosteler= 'Hosteler'
    Dayscholar= 'Day scholar'

    CSE = 'CSE'
    CS = 'CS'
    CSE_AIML = 'CSE(AIML)'
    CSE_DS = 'CSE(DS)'
    CSE_Hindi = 'CSE(Hindi)'
    AIML='AIML'
    IT ='IT'
    CSIT ='CSIT'
    ECE ='ECE'
    EN='EN'
    ME = 'ME'
    CIVIL = 'CIVIL'

    Second= '2'
    Third= '3'
    Fourth='4'

    one= '1'
    two = '2'
    three = '3'

    Residence=[
        (Hosteler, 'Hosteler'),
        (Dayscholar, 'Day scholar'),
    ]
    Gender = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]
    Branch = [
        (CSE, 'CSE'),
        (CS, 'CS'),
        (CSE_AIML, 'CSE(AIML)'),
        (CSE_DS, 'CSE(DS)'),
        (CSE_Hindi,'CSE(Hindi)'),
        (AIML,'AIML'),
        (IT,'IT'),
        (CSIT,'CSIT'),
        (ECE,'ECE'),
        (EN,'EN'),
        (ME, 'ME'),
        (CIVIL,'CIVIL'),
    ]
    Year=[
        (Second, '2'),
        (Third, '3'),
        (Fourth, '4'),
    ]
    section = [
         (one, '1'),
         (two, '2'),
         (three, '3'),
    ]
    name = models.CharField(max_length=50, null=False)
    created = models.DateTimeField(auto_now_add=True)
    student_no=models.IntegerField(validators=[MinValueValidator(2000000),MaxValueValidator(23999999),validate_Student_digits],unique=True, null=False)
    branch = models.CharField(max_length=10,null=False , choices=Branch)
    section = models.CharField(max_length=5,null = False, choices=section)
    email=models.EmailField(max_length=40,validators=[validate_akgec_email], null=False, unique=True )
    phone_number =models.IntegerField(validators=[MinValueValidator(1000000000),MaxValueValidator(9999999999), validate_Phone_digits], null=False)
    gender=models.CharField(max_length=50,null=False, choices=Gender)
    year = models.CharField(max_length=5,null = False, choices=Year)
    residence = models.CharField(max_length=15, null = False, choices=Residence)