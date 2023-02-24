from django.contrib import admin
from .models import Dataset, Protocol, Task, Activity, Parent, Child1, Child2

# Register your models here.
admin.site.register(Dataset)
admin.site.register(Protocol)
admin.site.register(Task)
admin.site.register(Activity)
admin.site.register(Parent)
admin.site.register(Child1)
admin.site.register(Child2)