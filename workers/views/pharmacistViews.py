from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
import sweetify
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import login_required
from django.utils.decorators import method_decorator
from workers.models.pharmacist import Pharmacist, PharmacistForm
from django.contrib.auth.models import User, Group
from workers.models.pharmacist import PharmacyAgentRegistrationForm
from workers.filters.pharmacist_filter import PharmacistFilter


# Create your views here.
"""
    declaration of some data
"""
pharmacist_list_template = 'workers/pharmacist/pharmacist_list.html'
create_pharmacist_template = 'workers/pharmacist/pharmacist_form.html'
success = 'Success!'
error = 'Error!'
error_message = 'Something Wrong Happened, please Try Again'


@method_decorator(login_required, name='dispatch')
class PharmacistList(ListView):
    model = Pharmacist
    template_name = pharmacist_list_template
    paginate_by = 5
    context_object_name = 'pharmacists'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["find"] = PharmacistFilter(
            self.request.GET, queryset=Pharmacist.objects.all().order_by("id"))
        return context

    def get_queryset(self):
        return PharmacistFilter(self.request.GET, queryset=Pharmacist.objects.all().order_by("id")).qs



@method_decorator(login_required, name='dispatch')
class PharmacistCreateView(CreateView):
    model = Pharmacist
    template_name = create_pharmacist_template
    form_class = PharmacistForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add"
        return context

    def get_success_url(self):
        sweetify.success(self.request, success, text='You have successfully Added Pharmacist', icon='success', timerProgressBar='true', timer=3000)
        return reverse_lazy('pharmacist_list')
    
    
def register_pharmacy_agent(request):
    form = PharmacyAgentRegistrationForm()
    if request.method == 'POST':
        form = PharmacyAgentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='pharmacy')
            user.groups.add(group)
            Pharmacist.objects.create(
                user=user,
                name=user.username,
                email = user.email,
            )
            messages.success(request, 'Pharmacist has been successfully registered')
            
            return redirect('create_pharmacy')
    
    context = {'form':form}
    return render(request, 'workers/pharmacist/register_pharmacy_agent.html', context)



    
@method_decorator(login_required, name='dispatch')
class PharmacistUpdate(UpdateView):
    model = Pharmacist
    form_class = PharmacistForm
    template_name = create_pharmacist_template
    context_object_name = 'pharmacist'

    def get_object(self):
        return Pharmacist.objects.get(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit"
        return context

    def get_success_url(self):
        sweetify.success(self.request, success, text='You have successfully Update Pharmacist info', icon='success', timerProgressBar='true', timer=3000)
        return reverse_lazy('pharmacist_list')


@login_required(login_url='/accounts/login')
def pharmacist_detail(request, id):
    pharmacist = get_object_or_404(Pharmacist, id=id)
    context = {
        'pharmacist': pharmacist,
    }
    return render(request, 'workers/pharmacist/pharmacist_detail.html', context)


@login_required(login_url='/accounts/login')
def delete_pharmacist(request, id):
    pharmacist = get_object_or_404(Pharmacist, id=id)
    pharmacist.delete()
    sweetify.success(request, success, text='You have successfully deleted pharmacist', icon='success', timerProgressBar='true', timer=3000)
    return redirect('pharmacist_list')



