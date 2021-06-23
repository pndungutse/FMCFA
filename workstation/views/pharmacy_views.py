from django.http import JsonResponse, HttpResponse, request
from workstation.utils import render_to_pdf
from django.template.loader import get_template
from beneficiary.models import Beneficiary
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from workstation.models.pharmacy import Pharmacy, PharmacyForm, Pharmacist
from workstation.models.hospital import Ordonance, Drug, DrugsIssuing, DrugsIssuingForm
from django.core.paginator import Paginator
import sweetify
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import login_required
from django.utils.decorators import method_decorator

phar_list_template = 'workstation/pharmacy_list.html'
create_phar_template = 'workstation/pharmacy_form.html'
success = 'Success!'
error = 'Error!'
error_message = 'Something Wrong Happened, please Try Again'

def pharmacyList(request):
    
    pharmacies = Pharmacy.objects.all()
    paginator = Paginator(pharmacies, 5) # Show 5 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'workstation/pharmacy_list.html', context)

@method_decorator(login_required, name='dispatch')
class PhamacyCreateView(CreateView):
    model = Pharmacy
    template_name = create_phar_template
    form_class = PharmacyForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add"
        return context

    def get_success_url(self):
        sweetify.success(self.request, success, text='You have successfully Added Pharmacy', icon='success', timerProgressBar='true', timer=3000)
        return reverse_lazy('pharmacy_list')
    
def pharmacyStatisticalReport(request):
    
    context = {}
    return render(request, 'workstation/pharmacyStatisticalReport.html', context)

def medecineProvision(request, pk_ben):
    
    beneficiary = Beneficiary.objects.get(id=pk_ben)
    pending_medecines = Ordonance.objects.filter(beneficiary=beneficiary, status='PENDING')
    
    context = {'pending_medecines':pending_medecines}
    return render(request, 'workstation/provideMedecine.html', context)


def print_ordonance_phar(request, pk):
    template = get_template('workstation/ordonance_phar.html')
    beneficiary = Beneficiary.objects.get(id=pk)
    pending_medecines = beneficiary.ordonance_set.filter(status='PENDING').order_by('hospital')
    
    context = {'beneficiary':beneficiary,'pending_medecines':pending_medecines}
    
    html = template.render(context)
    pdf= render_to_pdf('workstation/ordonance_phar.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Ordonance Paper for %s" %(beneficiary.name)
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def deliverMedecine(request, pk):
    ord_med = Ordonance.objects.get(id=pk)
    
    context = {'ord_med':ord_med}
    return render(request, 'workstation/deliverMedecine.html', context)

def saveDrugIssue(request, pk):   
    user = request.user
    pharmacist = Pharmacist.objects.get(user=user)
    pharmacy = Pharmacy.objects.get(agent=pharmacist)
    print(pharmacy)
    
    beneficiary = Beneficiary.objects.get(id=pk)
    print(beneficiary)
    
    try:
        ord_id = request.GET.get('ord_id')
        quantity = request.GET.get('quantity')
        drugg = request.GET.get('drug')
    except:
        ord_id = None
        quantity = None
        drugg = None
    if ord_id:
        ordSearched = ord_id
        ordonance = Ordonance.objects.get(id=ordSearched)
        print(ordonance) 
        if quantity:
            quantitySearched = float(quantity)
            if drugg:
                drugSearched = drugg
                drug = Drug.objects.get(id=drugSearched)
                totalPrice = quantitySearched * drug.unitPrice
                print(totalPrice)
                
                DrugsIssuing.objects.create(
                    pharmacy = pharmacy,
                    beneficiary = beneficiary,
                    drug = drug,
                    quantity = quantitySearched,
                    totalPrice = totalPrice
                )
                ordonance.status = 'DELIVERED'
                ordonance.save()
    sweetify.success(request, success, text='You have gave medecine to beneficiary', icon='success', timerProgressBar='true', timer=3000)        
    return redirect('list_beneficiary_phar')
