from datetime import datetime, timedelta
from re import template
import re
from workstation.models.hospital import Drug, DrugsIssuing, DrugsIssuingForm, Medical_Exam
import beneficiary
from django.http import JsonResponse, HttpResponse, request
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from workstation.models.hospital import Hospital, Pass, HospitalForm, Ordonance, OrdonanceForm, Medical_ExamForm, Medical_Exam, Suggestion, SuggestionForm
from workstation.models.pharmacy import Pharmacy, Pharmacist
from workers.models.hosAgent import HospitalAgent
from beneficiary.models import Beneficiary
from workstation.utils import render_to_pdf
from django.template.loader import get_template
from django.core.paginator import Paginator
import sweetify
from django.contrib import messages
from django.urls import reverse_lazy
# from django.contrib.auth.views import login_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.forms import inlineformset_factory
from django.db.models import Sum
import datetime

hos_list_template = 'workstation/hospital_list.html'
create_hos_template = 'workstation/hospital_form.html'
success = 'Success!'
error = 'Error!'
error_message = 'Something Wrong Happened, please Try Again'



def render_hospital_dashboard(request):
    user = request.user
    hospital_agent = HospitalAgent.objects.get(user=user)
    hospital = Hospital.objects.get(agent=hospital_agent)
    
    year =datetime.datetime.now().year
    
    january = Pass.objects.filter(date_created__year__gte=year, date_created__month=1, hospital=hospital).count()
    february = Pass.objects.filter(date_created__year__gte=year, date_created__month=2, hospital=hospital).count()
    march = Pass.objects.filter(date_created__year__gte=year, date_created__month=3, hospital=hospital).count()
    april = Pass.objects.filter(date_created__year__gte=year, date_created__month=4, hospital=hospital).count()
    may = Pass.objects.filter(date_created__year__gte=year, date_created__month=5, hospital=hospital).count()
    june = Pass.objects.filter(date_created__year__gte=year, date_created__month=6, hospital=hospital).count()
    july = Pass.objects.filter(date_created__year__gte=year, date_created__month=7, hospital=hospital).count()
    august = Pass.objects.filter(date_created__year__gte=year, date_created__month=8, hospital=hospital).count()
    september = Pass.objects.filter(date_created__year__gte=year, date_created__month=9, hospital=hospital).count()
    october = Pass.objects.filter(date_created__year__gte=year, date_created__month=10, hospital=hospital).count()
    november = Pass.objects.filter(date_created__year__gte=year, date_created__month=11, hospital=hospital).count()
    december = Pass.objects.filter(date_created__year__gte=year, date_created__month=12, hospital=hospital).count()

    context = {'hospital':hospital,
               'january':january, 'february':february, 'march':march, 'april':april, 'may':may,'june':june, 
               'july':july, 'august':august, 'september':september, 'october':october, 'november':november, 'december':december
               }
    return render(request, 'workers/hosAgent/hospitalDashboard.html', context)

def hospitalDetail(request, pk):
    hospital = Hospital.objects.get(id=pk)
    
    context = {'hospital':hospital}
    return render(request, 'hospitalDetail.html', context)

def delete_hospital(request, id):
    hospital = Hospital.objects.get(pk=id)
    hospital.delete()
    sweetify.success(request, success, text='You have successfully deleted hospital', icon='success', timerProgressBar='true', timer=3000)
    messages.success(request, 'Hospital has been deleted Successfully')
    return redirect('hospital_list')

def update_hospital(request, pk):
    user = request.user
    hospital = Hospital.objects.get(id=pk)
    form = HospitalForm(instance=hospital)
    title = 'Update'
    # form.fields['sector'].queryset = School.objects.filter(sector=sector.id)
    if request.method == 'POST':
        form = HospitalForm(request.POST, instance=hospital)
        if form.is_valid:
            form.save()
            sweetify.success(request, success, text='You have successfully updated hospital', icon='success', timerProgressBar='true', timer=3000) 
            messages.success(request, 'Hospital has been Updated Successfully')
            return redirect('hospital_list')
    context = {'form':form, 'title':title}
    return render(request, 'hospitalForm.html',context)
def adminReports(request):
    
    male = Beneficiary.objects.filter(gender='MALE').count()
    female = Beneficiary.objects.filter(gender='FEMALE').count()
    print(male)
    
    
    context = {'male':male,'female':female}
    return render(request, 'workstation/adminReports.html', context)

@login_required(login_url='/accounts/login')
@user_passes_test(lambda u: u.is_superuser)
def hospitalList(request):
    
    hospitals = Hospital.objects.all()
    paginator = Paginator(hospitals, 5) # Show 5 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'workstation/hospital_list.html', context)

# @method_decorator(login_required, name='dispatch')
class HospitalCreateView(CreateView):
    model = Hospital
    template_name = create_hos_template
    form_class = HospitalForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add"
        return context

    def get_success_url(self):
        sweetify.success(self.request, success, text='You have successfully Added Hospital', icon='success', timerProgressBar='true', timer=3000)
        return reverse_lazy('hospital_list')
    
def providePassToBeneficiary(request, pk):
    template = get_template('workstation/providePass.html')
    
    user = request.user
    hospital_agent = HospitalAgent.objects.get(user=user)
    hospital = Hospital.objects.get(agent=hospital_agent)
    beneficiary = Beneficiary.objects.get(id=pk)
    Pass.objects.create(
        hospital=hospital,
        beneficiary=beneficiary,
    )
    
    context = {'hospital':hospital, 'beneficiary':beneficiary}
    html = template.render(context)
    pdf= render_to_pdf('workstation/providePass.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Permission Paper for %s  %s" %(beneficiary.name, hospital.name)
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def provide_medical_exams(request, pk):
    beneficiary = Beneficiary.objects.get(id=pk)
    user = request.user
    hospital_agent = HospitalAgent.objects.get(user=user)
    hospital = Hospital.objects.get(agent=hospital_agent)
    
    form = Medical_ExamForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            medical_exam = form.save(commit=False)
            medical_exam.beneficiary = beneficiary
            medical_exam.hospital = hospital
            medical_exam.save()
            sweetify.success(request, success, text='You have successfully gave medical exam', icon='success', timerProgressBar='true', timer=3000)   
            return redirect(request.path)
    
    medical_exam_auth = Medical_Exam.objects.filter(hospital=hospital, beneficiary=beneficiary)
        
    context = {'form':form, 'beneficiary':beneficiary, 'medical_exam_auth':medical_exam_auth, 'hospital':hospital}
    return render(request, 'workstation/provide_medical_exams.html', context)

def provide_ordonance(request, pk):
    user = request.user
    hospital_agent = HospitalAgent.objects.get(user=user)
    hospital = Hospital.objects.get(agent=hospital_agent)
    
    beneficiary = Beneficiary.objects.get(id=pk)
    
    form = OrdonanceForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            ordonance = form.save(commit=False)
            ordonance.beneficiary = beneficiary
            ordonance.hospital = hospital
            ordonance.status = 'PENDING'
            ordonance.save()
            sweetify.success(request, success, text='You have successfully gave medical exam', icon='success', timerProgressBar='true', timer=3000)   
            return redirect(request.path)
        
    pending_medecines = beneficiary.ordonance_set.filter(status='PENDING', hospital=hospital)
    print(pending_medecines)
    context = {'form':form, 'beneficiary':beneficiary,'pending_medecines':pending_medecines, 'hospital':hospital}
    return render(request, 'workstation/provide_ordonance.html', context)

def print_ordonance(request, pk):
    template = get_template('workstation/ordonance.html')
    # user = request.user
    # hospital_agent = HospitalAgent.objects.get(user=user)
    # hospital = Hospital.objects.get(agent=hospital_agent)
    user=request.user
    hospital_agent = HospitalAgent.objects.get(user=user)
    hospital = Hospital.objects.get(agent=hospital_agent)
    
    beneficiary = Beneficiary.objects.get(id=pk)
    pending_medecines = beneficiary.ordonance_set.filter(status='PENDING', hospital=hospital).order_by('hospital')
    total =0
    # for medecine in pending_medecines:
    #     total += medecine.drug['unitPrice']
    #     print(total)
    context = {'beneficiary':beneficiary,'pending_medecines':pending_medecines, 'user':user, 'hospital':hospital}
    
    html = template.render(context)
    pdf= render_to_pdf('workstation/ordonance.html', context)
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


def hospitalStatisticalReport(request):
    user = request.user
    hospital_agent = HospitalAgent.objects.get(user=user)
    hospital = Hospital.objects.get(agent=hospital_agent)
    
    context = {'hospital':hospital}
    return render(request, 'workstation/hospitalStatisticalReport.html', context)

def benTreatmantHistory(request):
    template = get_template('beneficiary/benTreatmentHistory.html')
    user = request.user
    hospital_agent = HospitalAgent.objects.get(user=user)
    hospital = Hospital.objects.get(agent=hospital_agent)
    
    try:
        ben_code = request.GET.get('ben_code')
    except:
        ben_code = None
        
    if ben_code:
        ben_searched = ben_code
        beneficiary = Beneficiary.objects.get(ben_code=ben_searched)
        print(beneficiary)
        passes = Pass.objects.filter(beneficiary=beneficiary, hospital=hospital)
    
    context = {'passes':passes,'beneficiary':beneficiary,'hospital':hospital,'user':user}
    html = template.render(context)
    pdf= render_to_pdf('beneficiary/benTreatmentHistory.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Treatment history for %s at %s" %(beneficiary.name, hospital.name)
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def reportAllBeneficiaries(request):
    user = request.user
    template = get_template('workstation/allBeneficiariesPDF.html')
    beneficiaries = Beneficiary.objects.all()
    context = {'beneficiaries':beneficiaries, 'user':user}
    html = template.render(context)
    pdf= render_to_pdf('workstation/allBeneficiariesPDF.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "All beneficiaries registered"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def hos_parmaciesPDF(request):
    user = request.user
    template = get_template('workstation/hos_parmaciesPDF.html')
    hospitals = Hospital.objects.all()
    pharmacies = Pharmacy.objects.all()
    context = {'hospitals':hospitals,'pharmacies':pharmacies, 'user':user}
    html = template.render(context)
    pdf= render_to_pdf('workstation/hos_parmaciesPDF.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "All hospitals and pharmacies partners"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def medecinesAllowed(request):
    user = request.user
    template = get_template('workstation/medecinesAllowedPDF.html')
    drugs = Drug.objects.all()
    context = {'drugs':drugs, 'user':user}
    html = template.render(context)
    pdf= render_to_pdf('workstation/medecinesAllowedPDF.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "All beneficiaries registered"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def comapare2MonthsHos(request):
    template = get_template('compare2MonthsHos.html')
    user = request.user
    hospital_agent = HospitalAgent.objects.get(user=user)
    hospital = Hospital.objects.get(agent=hospital_agent)
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
                medical_exams_month1 = Medical_Exam.objects.filter(hospital=hospital, date_created__year__gte=yearSearched, date_created__month=month1Searched)
                medical_exams_month1Sum = Medical_Exam.objects.filter(hospital=hospital, date_created__year__gte=yearSearched, date_created__month=month1Searched).aggregate(Sum('exam__price')).get('exam__price__sum', 0.00)
                
                mdedical_exams_month2 = Medical_Exam.objects.filter(hospital=hospital, date_created__year__gte=yearSearched, date_created__month=month2Searched)
                mdedical_exams_month2Sum = Medical_Exam.objects.filter(hospital=hospital, date_created__year__gte=yearSearched, date_created__month=month2Searched).aggregate(Sum('exam__price')).get('exam__price__sum', 0.00)
            
    context = {'medical_exams_month1':medical_exams_month1, 'mdedical_exams_month2':mdedical_exams_month2, 'user':user, 'hospital':hospital,
               'medical_exams_month1Sum':medical_exams_month1Sum,'month1Selected': month1Searched, 'month2Searched':month2Searched,
               'mdedical_exams_month2Sum':mdedical_exams_month2Sum}
    pdf= render_to_pdf('compare2MonthsHos.html', context)
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
    
    
def addSuggestion(request, pk):
    user = request.user
    hospital_agent = HospitalAgent.objects.get(user=user)
    hospital = Hospital.objects.get(agent=hospital_agent)
    
    beneficiary = Beneficiary.objects.get(id=pk)
    
    title = 'Add'
    
    form = SuggestionForm(request.POST)
    if request.method == 'POST':
        if form.is_valid:
            suggestion = form.save(commit=False)
            suggestion.beneficiary = beneficiary
            suggestion.hospital = hospital
            suggestion.save()
            
            sweetify.success(request, success, text='You have successfully sent your suggestion', icon='success', timerProgressBar='true', timer=3000) 
            # messages.success(request, 'Hospital has been Updated Successfully')
            return redirect('hos_dashboard')
    context = {'form':form, 'title':title}
    return render(request, 'suggestionForm.html',context)
    
    
    
    


    
    
    
    

