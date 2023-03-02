from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView

from .models import Parent
from datasets.models import DatasetModel, DatasetField
from datasets.forms import ActivityForm
from .forms import  ParentForm, Child1Form, Child2Form


# Activities

def activity_view(request, pk):
    models = DatasetModel.objects.filter(dataset = pk, parent_model=True)
    context = {'models':models}
    return render(request, "data/dataset_activities.html", context)

class ActivityListView(ListView):
    model = Parent
    template_name = 'data/activity_list.html'

def activity_new(request):
    if request.method == 'POST':
        activity_form = ActivityForm(request.POST)
        parent_form = ParentForm(request.POST)
        child1_form = Child1Form(request.POST)
        child2_form = Child2Form(request.POST)
        if activity_form.is_valid() and parent_form.is_valid() and child1_form.is_valid() and child2_form.is_valid():
            activity=activity_form.save(commit=False)
            activity.created_by = request.user
            activity.save()
       
            parent=parent_form.save(commit=False)
            parent.activity = activity
            parent.updated_by = request.user
            parent.save()

            child1=child1_form.save(commit=False)
            child1.parent = parent
            child1.updated_by = request.user
            child1.save()

            child2=child2_form.save(commit=False)
            child2.parent = parent
            child2.updated_by = request.user
            child2.save()

            return redirect('activity_list')

    activity_form = ActivityForm(request.POST)
    parent_form = ParentForm(request.POST)
    child1_form = Child1Form(request.POST)
    child2_form = Child2Form(request.POST)
    context = {'activity_form':activity_form, 'parent_form':parent_form, 'child1_form':child1_form, 'child2_form':child2_form}
    return render(request, "data/activity_new.html", context)

def activity_edit(request, pk):
    parent = get_object_or_404(Parent, pk=pk)
    if request.method == 'POST':
        #activity_form = ActivityForm(request.POST)
        parent_form = ParentForm(request.POST, instance=parent)
        child1_form = Child1Form(request.POST)
        child2_form = Child2Form(request.POST)
        if parent_form.is_valid() and child1_form.is_valid() and child2_form.is_valid():
           
            parent=parent_form.save(commit=False)
            parent.updated_by = request.user
            parent.pk = None
            parent.save()

            child1=child1_form.save(commit=False)
            child1.updated_by = request.user
            child1.pk = None
            child1.save()

            child2=child2_form.save(commit=False)
            child2.updated_by = request.user
            child2.pk = None
            child2.save()
            
            return redirect('activity_list')

    parent_form = ParentForm(instance=parent)
    child1_form = Child1Form(instance=child1)
    child2_form = Child2Form(instance=child2)
    context = {'parent_form':parent_form, 'child1_form':child1_form, 'child2_form':child2_form}
    return render(request, "data/activity_new.html", context)