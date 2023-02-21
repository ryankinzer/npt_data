from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from locations.models import Location

# Create your models here.

class Activity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) # adds date at the creation of the record was: auto_now_add=True
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_by')
    location = models.ForeignKey(Location,default=1, null= True, blank=True, on_delete=models.CASCADE, verbose_name = "Location")

class AuditableModel(models.Model):
    #created_at = models.DateTimeField(auto_now_add=True) # adds date at the creation of the record was: auto_now_add=True
    #updated_at = models.DateTimeField(auto_now=True) 
    effective_date = models.DateTimeField(auto_now=True)# updates the value when ever the record is saved/updated
    status = models.CharField(max_length=10, choices=(("active", "Active"), ("inactive", "Inactive")), default="active")
    #created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_by')
    
    #record_id = models.AutoField(primary_key=False)
    #rowid
    #orderid

    class Meta:
        abstract = True
        ordering = ("-effective_date", "-created_at")

    def save(self, *args, **kwargs):
        if not self.pk: # if pk is blank set status to active
            self.status = "active"
        super().save(*args, **kwargs)
        self.__class__.objects.filter(pk=self.pk, status="active").exclude(effective_date=self.effective_date).update(status="inactive")

    @classmethod
    def create_snapshot(cls, original_model):
        new_model = cls()
        for field in original_model._meta.fields:
            setattr(new_model, field.name, getattr(original_model, field.name))
        new_model.pk = None
        new_model.effective_date = original_model.effective_date
        new_model.status = "active"
        new_model.updated_by = original_model.updated_by
        #new_model.updated_at = original_model.updated_at
        new_model.save()
        return new_model

class MyModel(AuditableModel):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if user:
            if not self.pk: # if self.pk is blank...set created by to user
                self.created_by = user
            self.updated_by = user
        super(MyModel, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('home')
		#return reverse('news_detail', args=(str(self.id)))
