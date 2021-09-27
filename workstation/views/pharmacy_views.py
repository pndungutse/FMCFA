from datetime import datetime, timedelta
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
from django.db.models import Sum


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

def pharmacyDetail(request, pk):
    pharmacy = Pharmacy.objects.get(id=pk)
    
    context = {'pharmacy':pharmacy}
    return render(request, 'pharmacyDetail.html', context)

def delete_pharmacy(request, id):
    pharmacy = Pharmacy.objects.get(pk=id)
    pharmacy.delete()
    sweetify.success(request, success, text='You have successfully deleted pharmacy', icon='success', timerProgressBar='true', timer=3000)
    messages.success(request, 'Pharmacy has been deleted Successfully')
    return redirect('pharmacy_list')

def update_pharmacy(request, pk):
    user = request.user
    pharmacy = Pharmacy.objects.get(id=pk)
    form = PharmacyForm(instance=pharmacy)
    title = 'Update'
    # form.fields['sector'].queryset = School.objects.filter(sector=sector.id)
    if request.method == 'POST':
        form = PharmacyForm(request.POST, instance=pharmacy)
        if form.is_valid:
            form.save()
            sweetify.success(request, success, text='You have successfully updated pharmacy', icon='success', timerProgressBar='true', timer=3000) 
            messages.success(request, 'Pharmacy has been Updated Successfully')
            return redirect('pharmacy_list')
    context = {'form':form, 'title':title}
    return render(request, 'pharmacyForm.html',context)

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
    user = request.user
    pharmacist = Pharmacist.objects.get(user=user)
    pharmacy = Pharmacy.objects.get(agent=pharmacist)
    context = {'pharmacy':pharmacy}
    return render(request, 'workstation/pharmacyStatisticalReport.html', context)

def medecineProvision(request, pk_ben):
    user = request.user
    pharmacist = Pharmacist.objects.get(user=user)
    pharmacy = Pharmacy.objects.get(agent=pharmacist)
    
    beneficiary = Beneficiary.objects.get(id=pk_ben)
    pending_medecines = Ordonance.objects.filter(beneficiary=beneficiary, status='PENDING')
    
    context = {'pending_medecines':pending_medecines, 'pharmacy':pharmacy}
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
    user = request.user
    pharmacist = Pharmacist.objects.get(user=user)
    pharmacy = Pharmacy.objects.get(agent=pharmacist)
    context = {'ord_med':ord_med, 'pharmacy':pharmacy}
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


def lastWeekPharPDF(request):
    template = get_template('lastWeekReportPhar.html')
    user = request.user
    pharmacist = Pharmacist.objects.get(user=user)
    pharmacy = Pharmacy.objects.get(agent=pharmacist)
    last_week = datetime.today() - timedelta(days=7)
    
    drugsLastWeek = DrugsIssuing.objects.filter(pharmacy=pharmacy, date_created__gte=last_week)
    drugsLastWeekTotalSum = DrugsIssuing.objects.filter(pharmacy=pharmacy, date_created__gte=last_week).aggregate(Sum('totalPrice')).get('totalPrice', 0.00)
    
    context = {'drugsLastWeek':drugsLastWeek, 'user':user, 'drugsLastWeekTotalSum':drugsLastWeekTotalSum,
               'user':user, 'pharmacy':pharmacy}
    html = template.render(context)
    pdf= render_to_pdf('lastWeekReportPhar.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Last Week Report for %s" %(pharmacy)
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def lastMonthPharPDF(request):
    template = get_template('lastMonthReportPhar.html')
    user = request.user
    pharmacist = Pharmacist.objects.get(user=user)
    pharmacy = Pharmacy.objects.get(agent=pharmacist)
    last_month = datetime.today() - timedelta(days=30)
    
    drugsLastMonth = DrugsIssuing.objects.filter(pharmacy=pharmacy, date_created__gte=last_month)
    drugsLastMonthTotalSum = DrugsIssuing.objects.filter(pharmacy=pharmacy, date_created__gte=last_month).aggregate(Sum('totalPrice')).get('totalPrice__sum', 0.00)
    
    context = {'drugsLastMonth':drugsLastMonth, 'user':user, 'drugsLastMonthTotalSum':drugsLastMonthTotalSum,
               'user':user, 'pharmacy':pharmacy}
    html = template.render(context)
    pdf= render_to_pdf('lastMonthReportPhar.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Last Month Report for %s" %(pharmacy)
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"


def lastYearPharPDF(request):
    template = get_template('lastYearReportPhar.html')
    user = request.user
    pharmacist = Pharmacist.objects.get(user=user)
    pharmacy = Pharmacy.objects.get(agent=pharmacist)
    last_year = datetime.today() - timedelta(days=365)
    
    drugsLastYear = DrugsIssuing.objects.filter(pharmacy=pharmacy, date_created__gte=last_year)
    drugsLastYearTotalSum = DrugsIssuing.objects.filter(pharmacy=pharmacy, date_created__gte=last_year).aggregate(Sum('totalPrice')).get('totalPrice__sum', 0.00)
    
    context = {'drugsLastYear':drugsLastYear, 'user':user, 'drugsLastYearTotalSum':drugsLastYearTotalSum,
               'user':user, 'pharmacy':pharmacy}
    html = template.render(context)
    pdf= render_to_pdf('lastYearReportPhar.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Last Year Report for %s" %(pharmacy)
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def comapare2MonthsPhar(request):
    template = get_template('compare2MonthsPhar.html')
    user = request.user
    pharmacist = Pharmacist.objects.get(user=user)
    pharmacy = Pharmacy.objects.get(agent=pharmacist)
    try:
        year = request.GET.get('year')
        month1 = request.GET.get('month1')
        month2 = request.GET.get('month2')
    except:
        year = None
        month1 = None
        month2 = None
        
    if year:
        yearSearched = year
        if month1:
            month1Searched = month1
            if month2:
                month2Searched = month2
                drugs_month1 = DrugsIssuing.objects.filter(pharmacy=pharmacy, date_created__year__gte=yearSearched, date_created__month=month1Searched)
                drugs_month1Sum = DrugsIssuing.objects.filter(pharmacy=pharmacy, date_created__year__gte=yearSearched, date_created__month=month1Searched).aggregate(Sum('totalPrice')).get('totalPrice__sum', 0.00)
                
                drugs_month2 = DrugsIssuing.objects.filter(pharmacy=pharmacy, date_created__year__gte=yearSearched, date_created__month=month2Searched)
                drugs_month2Sum = DrugsIssuing.objects.filter(pharmacy=pharmacy, date_created__year__gte=yearSearched, date_created__month=month2Searched).aggregate(Sum('totalPrice')).get('totalPrice__sum', 0.00)
            
    context = {'drugs_month1':drugs_month1, 'drugs_month2':drugs_month2, 'user':user, 'pharmacy':pharmacy,
               'drugs_month1Sum':drugs_month1Sum,'month1Selected': month1Searched, 'month2Searched':month2Searched,
               'drugs_month2Sum':drugs_month2Sum}
    pdf= render_to_pdf('compare2MonthsPhar.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Medical Exam Provided Comparison"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def datePharPDF(request):
    template = get_template('searchedDateReportPhar.html')
    user = request.user
    pharmacist = Pharmacist.objects.get(user=user)
    pharmacy = Pharmacy.objects.get(agent=pharmacist)
    # last_year = datetime.today() - timedelta(days=365)
    
    try:
        date_search = request.GET.get('date_search')
    except:
        date_search = None
        
    if date_search:
        date_searched = date_search
        # todaysDate = datetime.today()
        # print(date_searched)
        # print(todaysDate.date())
    
    drugsDateSearchedYear = DrugsIssuing.objects.filter(pharmacy=pharmacy, date_created__date=date_searched)
    drugsDateSearchedTotalSum = DrugsIssuing.objects.filter(pharmacy=pharmacy, date_created__date=date_searched).aggregate(Sum('totalPrice')).get('totalPrice__sum', 0.00)
    
    context = {'drugsDateSearchedYear':drugsDateSearchedYear, 'user':user, 'drugsDateSearchedTotalSum':drugsDateSearchedTotalSum,
               'user':user, 'pharmacy':pharmacy, 'date_searched':date_searched}
    html = template.render(context)
    pdf= render_to_pdf('searchedDateReportPhar.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Date Searched Report for %s" %(pharmacy)
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"
