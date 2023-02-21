from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView

from .models import MyModel
from .forms import MyModelForm

# Create your views here.
class AuditableMixin(object,):

    def form_valid(self, form):
        if not form.instance.created_by: # if new record...form created_by is blank
            form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        #form.instance.pk = None
        return super(AuditableMixin, self).form_valid(form)

# def home(request):
#     return render(request, 'home.html', {})

class MyModelCreateView(AuditableMixin, CreateView):
    model = MyModel
    form_class = MyModelForm
    template_name = 'data/model_form.html'

class MyModelUpdateView(AuditableMixin, UpdateView):
    model = MyModel
    form_class = MyModelForm
    template_name = 'data/model_form.html'

    # def form_valid(self, form):
    #     obj = form.save(commit=False)
    #     obj.pk = None
    #     return super(MyModelUpdateView, self).form_valid(form)

class MyModelListView(ListView):
    model = MyModel
    template_name = 'home.html'
