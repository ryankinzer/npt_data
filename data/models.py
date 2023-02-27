from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datasets.models import AuditParent

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
        
    def __str__(self):
        return self.id
    
    def get_absolute_url(self):
        return reverse('parent_list')

class AuditChild(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    effective_date = models.DateTimeField(auto_now=True)# updates the value when ever the record is saved/updated
    active_status = models.CharField(max_length=10, choices=(("active", "Active"), ("inactive", "Inactive")), default="active")
    row_id = models.IntegerField()

    class Meta:
        abstract = True
        ordering = ('-parent', "-effective_date", "active_status")

    def save(self, *args, **kwargs):
        if not self.pk: # if pk is blank set status to active
            self.active_status = "active"
        super().save(*args, **kwargs)
        self.__class__.objects.filter(parent_id=self.parent_id, active_status="active", row_id=self.row_id).exclude(effective_date=self.effective_date).update(active_status="inactive")


class Child1(AuditChild):
    feature = models.CharField(max_length=25, choices=(("Redd","Redd"), ("Live Fish", "Live Fish")), default="Redd")
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