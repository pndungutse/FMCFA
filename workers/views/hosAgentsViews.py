from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
import sweetify
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import login_required
from django.utils.decorators import method_decorator
from workers.models.hosAgent import HospitalAgent, HospitalAgentForm, HospitalAgentRegistrationForm
from workers.filters.hosAgent_filter import HospitalAgentFilter


# Create your views here.
"""
    declaration of some data
"""
hosAgent_list_template = 'workers/hosAgent/hosAgent_list.html'
create_hosAgent_template = 'workers/hosAgent/hosAgent_form.html'
success = 'Success!'
error = 'Error!'
error_message = 'Something Wrong Happened, please Try Again'


@method_decorator(login_required, name='dispatch')
class HospitalAgentList(ListView):
    model = HospitalAgent
    template_name = hosAgent_list_template
    paginate_by = 5
    context_object_name = 'hospitalAgents'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["find"] = HospitalAgentFilter(
            self.request.GET, queryset=HospitalAgent.objects.all().order_by("id"))
        return context

    def get_queryset(self):
        return HospitalAgentFilter(self.request.GET, queryset=HospitalAgent.objects.all().order_by("id")).qs



@method_decorator(login_required, name='dispatch')
class HospitalAgentCreateView(CreateView):
    model = HospitalAgent
    template_name = create_hosAgent_template
    form_class = HospitalAgentForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add"
        return context

    def get_success_url(self):
        sweetify.success(self.request, success, text='You have successfully Added HospitalAgent', icon='success', timerProgressBar='true', timer=3000)
        return reverse_lazy('hospitalAgent_list')
    
def register_hospital_agent(request):
    form = HospitalAgentRegistrationForm()
    if request.method == 'POST':
        form = HospitalAgentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='hospital')
            user.groups.add(group)
            HospitalAgent.objects.create(
                user=user,
                name=user.username,
                email = user.email,
            )
            messages.success(request, 'Hospital Agent has been successfully registered')
            
            return redirect('create_hospital')
    
    context = {'form':form}
    return render(request, 'workers/hosAgent/register_hospital_agent.html', context)
        
    
    



    
@method_decorator(login_required, name='dispatch')
class HospitalAgentUpdate(UpdateView):
    model = HospitalAgent
    form_class = HospitalAgentForm
    template_name = create_hosAgent_template
    context_object_name = 'hospitalAgent'

    def get_object(self):
        return HospitalAgent.objects.get(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit"
        return context

    def get_success_url(self):
        sweetify.success(self.request, success, text='You have successfully Update HospitalAgent info', icon='success', timerProgressBar='true', timer=3000)
        return reverse_lazy('hospitalAgent_list')


@login_required(login_url='/accounts/login')
def hospitalAgent_detail(request, id):
    hospitalAgent = get_object_or_404(HospitalAgent, id=id)
    context = {
        'hospitalAgent': hospitalAgent,
    }
    return render(request, 'workers/hosAgent/hosAgent_detail.html', context)


@login_required(login_url='/accounts/login')
def delete_hospitalAgent(request, id):
    hosAgent = get_object_or_404(HospitalAgent, id=id)
    hosAgent.delete()
    sweetify.success(request, success, text='You have successfully deleted Hospital Agent', icon='success', timerProgressBar='true', timer=3000)
    return redirect('hospitalAgent_list')
