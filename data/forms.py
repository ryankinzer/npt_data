from django import forms
from django.forms import ModelForm
from .models import Parent, Child1, Child2

class ParentForm(ModelForm):
    class Meta:
        model = Parent
        fields = ['protocol', 'task', 'location', 'publish_status', 'survey_date', 'species', 'surveyors', 'survey_type', 'survey_method']

class Child1Form(ModelForm):
    class Meta:
        model = Child1
        fields = ['feature_type', 'count', 'wpt_name', 'lat', 'long']

class Child2Form(ModelForm):
    class Meta:
        model = Child2
        fields = ['sample_id', 'sex', 'fork_length', 'lat', 'long']

