
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from .forms import DatasetForm, DatasetModelFormSet, DatasetFieldFormSet, ProtocolForm, TaskForm

from .models import Dataset, DatasetModel, Protocol, Task
 
def home(request):
    return render(request, 'home.html', {})

# Dataset Views

class DatasetInline():
    form_class = DatasetForm
    model = Dataset
    template_name = "datasets/dataset_create_or_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('datasets:list_datasets')

    def formset_models_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        models = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for model in models:
            model.dataset = self.object
            model.save()

class DatasetCreate(DatasetInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(DatasetCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'models': DatasetModelFormSet(prefix='models'),
            }
        else:
            return {
                'models': DatasetModelFormSet(self.request.POST or None, self.request.FILES or None, prefix='models'),
            }


class DatasetUpdate(DatasetInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(DatasetUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'models': DatasetModelFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='models'),
        }
    
class DatasetList(ListView):
    model = Dataset
    template_name = "datasets/dataset_list.html"
    context_object_name = "datasets"

def delete_model(request, pk):
    try:
        model = DatasetModel.objects.get(id=pk)
    except DatasetModel.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('datasets:update_dataset', pk=model.dataset.id)

    model.delete()
    messages.success(
            request, 'Image deleted successfully'
            )
    return redirect('datasets:update_dataset', pk=model.dataset.id)

def update_fields(request, pk):
    model = get_object_or_404(DatasetModel, pk=pk)
    # model = DatasetModel.objects.get(pk=pk)
    if request.method == 'POST':
        formset = DatasetFieldFormSet(request.POST, instance=model, prefix='fields')
        
        if formset.is_valid():
            formset.save(commit=True)
            return redirect('datasets:update_dataset', pk=model.dataset.id)
        
    formset = DatasetFieldFormSet(instance=model, prefix='fields')

    context = {'model':model, 'formset':formset}
    return render(request, "datasets/model_detail.html", context)

class ProtocolList(ListView):
    model = Protocol
    template_name = 'datasets/protocol_list.html'
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model.__name__
        return context

class ProtocolCreate(CreateView):
    model = Protocol
    form_class = ProtocolForm
    template_name = 'datasets/protocol_create_or_update.html'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model.__name__
        return context

class ProtocolUpdate(UpdateView):
    model = Protocol
    form_class = ProtocolForm
    template_name = 'datasets/protocol_create_or_update.html'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model.__name__
        return context

class TaskList(ListView):
    model = Task
    template_name = 'datasets/task_list.html'
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model.__name__
        return context

class TaskCreate(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'datasets/protocol_create_or_update.html'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model.__name__
        return context

class TaskUpdate(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'datasets/protocol_create_or_update.html'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model.__name__
        return context

