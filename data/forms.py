from django.forms import ModelForm
from .models import Dataset, Protocol, Task, Activity, Parent, Child1, Child2


class DatasetForm(ModelForm):
    class Meta:
        model = Dataset
        fields = ['name', 'description']

class ProtocolForm(ModelForm):
    class Meta:
        model = Protocol
        fields = ['name', 'description', 'date_started', 'date_ended', 'url']

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name']

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['dataset']

class ParentForm(ModelForm):
    class Meta:
        model = Parent
        fields = ['protocol', 'task', 'location', 'publish_status', 'survey_date', 'species', 'surveyors', 'survey_type', 'survey_method']

class Child1Form(ModelForm):
    class Meta:
        model = Child1
        fields = ['feature', 'count', 'wpt_name', 'lat', 'long']

class Child2Form(ModelForm):
    class Meta:
        model = Child2
        fields = ['sample_id', 'sex', 'fork_length', 'lat', 'long']