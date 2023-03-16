from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datasets.models import AuditParent, AuditChild

# Create your models here.

class Parent(AuditParent):
    survey_date = models.DateField()
    species = models.CharField(max_length = 20, choices=(("Sp/sm Chinook", "Sp/sm Chinook"), ("Fall Chinook", "Fall Chinook"), ("Coho", "Coho"), ("Sockeye", "Sockeye"), ("Steelhead", "Steelhead")), default= "Sp/sm Chinook")
    surveyors = models.CharField(max_length = 50)
    survey_type = models.CharField(max_length=25, choices=(("Redd and Carcass", "Redd and Carcass"), ("Redd", "Redd"), ("Carcass", "Carcass")), default="Redd and Carcass")
    survey_method = models.CharField(max_length = 25, choices=(("Ground", "Ground"), ("Helicopter","Helicopter"), ("UAV", "UAV")), default="Ground")

    # def save(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     if user:
    #         if not self.pk: # if self.pk is blank...set created by to user
    #             self.updated_by = user
    #     super(Parent, self).save(*args, **kwargs)
    
    # def get_fields(self):
    #         return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]
        
    def __str__(self):
        return str(self.id)

class Child1(AuditChild):
    feature_type = models.CharField(max_length=25, choices=(("Redd","Redd"), ("Live Fish", "Live Fish")), default="Redd")
    count = models.IntegerField()
    wpt_name = models.CharField(max_length = 10)
    lat = models.CharField(max_length=20, blank = True, null=True)
    long = models.CharField(max_length=20, blank = True, null=True)

class Child2(AuditChild):
    sample_id = models.CharField(max_length=30, blank=True, null=True)
    sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female'), ('U', 'Unknown')), default = 'M')
    fork_length = models.IntegerField()
    lat = models.CharField(max_length=20, blank = True, null=True)
    long = models.CharField(max_length=20, blank = True, null=True)


class TrapHeader(AuditParent):
    trap_date = models.DateField()

    def __str__(self):
        return str(self.id)
    
class TrapDetail(AuditChild):
    species = models.CharField(max_length=30)

    def __str__(self):
        return str(self.id)

