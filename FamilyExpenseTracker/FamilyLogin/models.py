from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class FamilyMembers(models.Model):
    familyLead = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    income = models.FloatField(max_length=5000000000000000)

    def __str__(self):
        return self.firstname


class Expenses(models.Model):
    familyLead = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(FamilyMembers,on_delete=models.CASCADE)
    purpose = models.CharField(max_length=100)
    expense = models.FloatField(max_length=100000000000000000)
    date = models.DateField(blank=True,null=True)

    def __str__(self):
        return str(self.name)