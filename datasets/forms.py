# datasets/forms.py
from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import Dataset, DatasetModel, DatasetField, Protocol, Task, Activity

# Dataset Forms
class DatasetForm(forms.ModelForm):

    class Meta:
        model = Dataset
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
        }

class DatasetModelForm(forms.ModelForm):

    class Meta:
        model = DatasetModel
        fields = ('model_name', 'parent_model')

DatasetModelFormSet = inlineformset_factory(
    Dataset, DatasetModel, form=DatasetModelForm,
    extra=1, can_delete=False, can_delete_extra=True
)


class DatasetFieldForm(ModelForm):
    class Meta:
        model = DatasetField
        fields = ('field_name', 'description', 'units', 'data_type', 'form_type', 'validation', 'possible_values', 'order')
        exclude = ('id', 'dataset_model',)

DatasetFieldFormSet = inlineformset_factory(
    DatasetModel,
    DatasetField,
    form=DatasetFieldForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True)



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