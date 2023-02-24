from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from locations.models import Location

# Create your models here.

class Dataset(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('dataset_list')

class Protocol(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date_started = models.DateField()
    date_ended = models.DateField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Activity(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) # adds date at the creation of the record was: auto_now_add=True
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if user:
            if not self.pk: # if self.pk is blank...set created by to user
                self.created_by = user
        super(Activity, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.status

class AuditParent(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, default=1, null= True, blank=True, on_delete=models.CASCADE, verbose_name = "Location")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    effective_date = models.DateTimeField(auto_now=True)# updates the value when ever the record is saved/updated
    active_status = models.CharField(max_length=10, choices=(("active", "Active"), ("inactive", "Inactive")), default="active")
    publish_status = models.CharField(max_length=10, choices=(("publish", "Publish"), ("draft", "Draft")), default="draft")

    class Meta:
        abstract = True
        ordering = ('-activity', "-effective_date", "active_status")

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if user:
            self.updated_by = user
        if not self.pk: # if pk is blank set status to active
            self.active_status = "active"
        super().save(*args, **kwargs)
        self.__class__.objects.filter(activity_id=self.activity_id, active_status="active").exclude(effective_date=self.effective_date).update(active_status="inactive")

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
