from django.shortcuts import render, redirect, get_object_or_404
import sweetify
from django.contrib import messages
from django.urls import reverse_lazy
# from django.contrib.auth.views import login_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.decolator import unauthenticated_user, allowed_users
from beneficiary.models import Beneficiary,BeneficiaryForm
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from beneficiary.filters.beneficiary_filter import BeneficiaryFilter
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
"""
    declaration of some data
"""
success = 'Success!'
error = 'Error!'
error_message = 'Something Wrong Happened, please Try Again'

# @login_required(login_url='/accounts/login')
# @user_passes_test(lambda u: u.is_superuser)
class BeneficiaryCreateView(CreateView):
    model = Beneficiary
    class_form = BeneficiaryForm
    fields = '__all__'
    success_url = "list"
    template_name = "beneficiary/register_beneficiary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add"
        return context

    def get_success_url(self):
        sweetify.success(self.request, success, text='You have successfully Added Benificiary', icon='success', timerProgressBar='true', timer=3000)
        return reverse_lazy('list_beneficiary')

# @login_required(login_url='/accounts/login')
# @user_passes_test(lambda u: u.is_superuser)
def beneficiaryDetailView(request, pk):
    beneficiary = Beneficiary.objects.get(id=pk)
    context = {'beneficiary':beneficiary}
    return render(request, 'beneficiary/view_beneficiary.html', context)

def beneficiaryDetailViewHos(request, pk):
    beneficiary = Beneficiary.objects.get(id=pk)
    context = {'beneficiary':beneficiary}
    return render(request, 'beneficiary/view_beneficiary_hos.html', context)

def beneficiaryDetailViewPhar(request, pk):
    beneficiary = Beneficiary.objects.get(id=pk)
    context = {'beneficiary':beneficiary}
    return render(request, 'beneficiary/view_beneficiaryPhar.html', context)


# @login_required(login_url='/accounts/login')
# @user_passes_test(lambda u: u.is_superuser)
class BeneficiaryListView(ListView):
    model = Beneficiary
    paginate_by = 5
    context_object_name = 'beneficiaries'
    template_name = "beneficiary/beneficiary_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["find"] = BeneficiaryFilter(
            self.request.GET, queryset=Beneficiary.objects.all().order_by("id"))
        return context

    def get_queryset(self):
        return BeneficiaryFilter(self.request.GET, queryset=Beneficiary.objects.all().order_by("id")).qs

# @login_required(login_url='/accounts/login')
# @allowed_users(allowed_roles=['hospital'])
class BeneficiaryListViewHospital(ListView):
    model = Beneficiary
    paginate_by = 5
    context_object_name = 'beneficiaries'
    template_name = "beneficiary/beneficiary_list_hos.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["find"] = BeneficiaryFilter(
            self.request.GET, queryset=Beneficiary.objects.all().order_by("id"))
        return context

    def get_queryset(self):
        return BeneficiaryFilter(self.request.GET, queryset=Beneficiary.objects.all().order_by("id")).qs
    
# @login_required(login_url='/accounts/login')
# @allowed_users(allowed_roles=['pharmacy'])
class BeneficiaryListViewPharmacy(ListView):
    model = Beneficiary
    paginate_by = 5
    context_object_name = 'beneficiaries'
    template_name = "beneficiary/beneficiary_list_phar.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["find"] = BeneficiaryFilter(
            self.request.GET, queryset=Beneficiary.objects.all().order_by("id"))
        return context

    def get_queryset(self):
        return BeneficiaryFilter(self.request.GET, queryset=Beneficiary.objects.all().order_by("id")).qs

# @login_required(login_url='/accounts/login')
# @user_passes_test(lambda u: u.is_superuser)
class BeneficiaryUpdateView(UpdateView):
    model = Beneficiary
    fields = '__all__'
    success_url = "view"
    template_name = 'beneficiary/update_beneficiary.html'
    context_object_name = 'beneficiary'

    def get_object(self):
        return Beneficiary.objects.get(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit"
        return context

    def get_success_url(self):
        sweetify.success(self.request, success, text='You have successfully Update Beneficiary info', icon='success', timerProgressBar='true', timer=3000)
        return reverse_lazy('list_beneficiary')

# @login_required(login_url='/accounts/login')
# @user_passes_test(lambda u: u.is_superuser)
def delete_beneficiary(request, id):
    beneficiary = get_object_or_404(Beneficiary, id=id)
    beneficiary.delete()
    sweetify.success(request, success, text='You have successfully deleted pharmacist', icon='success', timerProgressBar='true', timer=3000)
    return redirect('list_beneficiary')


def deleteBeneficiary(request, id):
    beneficiary = Beneficiary.objects.get(pk=id)
    beneficiary.delete()
    sweetify.success(request, success, text='You have successfully deleted beneficiary', icon='success', timerProgressBar='true', timer=3000)
    messages.success(request, 'Beneficiary has been deleted Successfully')
    return redirect('list_beneficiary')

def update_beneficiary(request, pk):
    user = request.user
    beneficiary = Beneficiary.objects.get(id=pk)
    form = BeneficiaryForm(instance=beneficiary)
    title = 'Update'
    # form.fields['sector'].queryset = School.objects.filter(sector=sector.id)
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST, instance=beneficiary)
        if form.is_valid:
            form.save()
            sweetify.success(request, success, text='You have successfully updated beneficiary', icon='success', timerProgressBar='true', timer=3000) 
            messages.success(request, 'Beneficiary has been Updated Successfully')
            return redirect('list_beneficiary')
    context = {'form':form, 'title':title}
    return render(request, 'beneficiaryUpdateForm.html',context)