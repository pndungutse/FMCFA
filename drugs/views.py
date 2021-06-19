from django.shortcuts import render
from workstation.models.hospital import DrugsIssuing, drugForm
from django.views.generic import CreateView, ListView, UpdateView, DetailView

# Create your views here.
class DrugCreateView(CreateView):
    model = DrugsIssuing
    class_form = drugForm
    fields = '__all__'
    success_url = "list"
    template_name = "drugs/register_drug.html"

class DrugDetailView(DetailView):
    model = DrugsIssuing
    template_name = "drugs/view_drug.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class DrugListView(ListView):
    model = DrugsIssuing
    context_object_name = 'drugs'
    template_name = "drugs/drugsissuing_list.html"
    
class DrugUpdateView(UpdateView): 
    model = DrugsIssuing
    fields = '__all__'
    success_url = "view"
    template_name = 'drugs/update_drug.html'