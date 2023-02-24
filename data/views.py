from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView

from .models import Dataset, Parent
from .forms import DatasetForm, ActivityForm, ParentForm

# Create your views here.
# class AuditableMixin(object,):

#     def form_valid(self, form):
#         #if not form.instance.created_by: # if new record...form created_by is blank
#         #    form.instance.created_by = self.request.user
#         form.instance.updated_by = self.request.user
#         form.instance.pk = None
#         return super(AuditableMixin, self).form_valid(form)

# def home(request):
#     return render(request, 'home.html', {})

# class ParentCreateView(AuditableMixin, CreateView):
#     model = Parent
#     form_class = ParentForm
#     template_name = 'data/model_form.html'

# class ParentUpdateView(AuditableMixin, UpdateView):
#     model = Parent
#     form_class = ParentForm
#     template_name = 'data/model_form.html'

class DatasetList(ListView):
    model = Dataset
    template_name = 'data/dataset_list.html'

class DatasetCreate(CreateView):
    model = Dataset
    template_name = 'data/dataset_new.html'
    fields = '__all__'

class ActivityListView(ListView):
    model = Parent
    template_name = 'data/activity_list.html'

def activity_new(request):
    if request.method == 'POST':
        activity_form = ActivityForm(request.POST)
        parent_form = ParentForm(request.POST)
        if activity_form.is_valid() and parent_form.is_valid():
            activity=activity_form.save(commit=False)
            activity.created_by = request.user
            activity.save()
       
            parent=parent_form.save(commit=False)
            parent.activity = activity
            parent.updated_by = request.user
            parent.save()
            return redirect('activity_list')

    activity_form = ActivityForm(request.POST)
    parent_form = ParentForm(request.POST)
    context = {'activity_form':activity_form, 'parent_form':parent_form}
    return render(request, "data/activity_new.html", context)

def activity_edit(request, pk):
    parent = get_object_or_404(Parent, pk=pk)
    if request.method == 'POST':
        #activity_form = ActivityForm(request.POST)
        parent_form = ParentForm(request.POST, instance=parent)
        if parent_form.is_valid():
           
            parent=parent_form.save(commit=False)
            parent.updated_by = request.user
            parent.pk = None
            parent.save()
            return redirect('activity_list')

    parent_form = ParentForm(instance=parent)
    context = {'parent_form':parent_form}
    return render(request, "data/activity_new.html", context)