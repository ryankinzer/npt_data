from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from locations.models import Location

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=150)
    short_description = models.TextField(max_length=100)

    def __str__(self):
        return self.title


class Image(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True
        )
    image = models.ImageField(blank=True, upload_to='images')

    def __str__(self):
        return self.product.title


class Variant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
        )
    size = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.product.title
    
# Task should be imported from other app
class Task(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

# Dataset Metadata

class Dataset(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name

      
class DatasetModel(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, null=True)
    model_name = models.CharField(max_length=100)
    parent_model = models.BooleanField(default=False)
    def __str__(self):
        return self.model_name #dataset.name
    
class DatasetField(models.Model):
    dataset_model = models.ForeignKey(DatasetModel, on_delete=models.CASCADE, null=True)
    field_name = models.CharField(max_length=100)
    description = models.CharField(max_length = 255, blank=True, null=True)
    units = models.CharField(max_length=2)
    data_type = models.CharField(max_length=20)
    form_type = models.CharField(max_length=20)
    validation = models.CharField(max_length=100)
    possible_values = models.CharField(max_length=100)
    order = models.IntegerField()

    def __str__(self):
        return self.field_name
    
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


# Dataset Auditting

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