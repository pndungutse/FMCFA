from datetime import datetime, timedelta
from workstation.utils import render_to_pdf
from django.template.loader import get_template
from django.http import JsonResponse, HttpResponse, request
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
from workstation.models.hospital import Medical_Exam, DrugsIssuing, Hospital
from django.db.models import Sum



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

def lastWeekAdminPDF(request):
    template = get_template('lastWeekReport.html')
    user = request.user
    last_week = datetime.today() - timedelta(days=7)
    
    examsLastWeek = Medical_Exam.objects.filter(date_created__gte=last_week)
    examsLastWeekTotalSum = Medical_Exam.objects.filter(date_created__gte=last_week).aggregate(Sum('exam__price')).get('exam__price__sum', 0.00)
    
    drugsLastWeek = DrugsIssuing.objects.filter(date_created__gte=last_week)
    drugsLastWeekTotalSum = DrugsIssuing.objects.filter(date_created__gte=last_week).aggregate(Sum('totalPrice')).get('totalPrice__sum')
    context = {'examsLastWeek':examsLastWeek, 'user':user, 'examsLastWeekTotalSum':examsLastWeekTotalSum,
               'drugsLastWeek':drugsLastWeek, 'drugsLastWeekTotalSum':drugsLastWeekTotalSum}
    html = template.render(context)
    pdf= render_to_pdf('lastWeekReport.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Last Week Report"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def lastMonthAdminPDF(request):
    template = get_template('lastMonthReport.html')
    user = request.user
    last_month = datetime.today() - timedelta(days=30)
    
    examsLastMonth = Medical_Exam.objects.filter(date_created__gte=last_month)
    examsLastMonthTotalSum = Medical_Exam.objects.filter(date_created__gte=last_month).aggregate(Sum('exam__price')).get('exam__price__sum', 0.00)
    
    drugsLastMonth = DrugsIssuing.objects.filter(date_created__gte=last_month)
    drugsLastMonthTotalSum = DrugsIssuing.objects.filter(date_created__gte=last_month).aggregate(Sum('totalPrice')).get('totalPrice__sum')
    context = {'examsLastMonth':examsLastMonth, 'user':user, 'examsLastMonthTotalSum':examsLastMonthTotalSum,
               'drugsLastMonth':drugsLastMonth, 'drugsLastMonthTotalSum':drugsLastMonthTotalSum}
    html = template.render(context)
    pdf= render_to_pdf('lastMonthReport.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Last Month Report"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def lastYearAdminPDF(request):
    template = get_template('lastYearReport.html')
    user = request.user
    last_year = datetime.today() - timedelta(days=365)
    
    examsLastYear = Medical_Exam.objects.filter(date_created__gte=last_year)
    examsLastYearTotalSum = Medical_Exam.objects.filter(date_created__gte=last_year).aggregate(Sum('exam__price')).get('exam__price__sum', 0.00)
    
    drugsLastYear = DrugsIssuing.objects.filter(date_created__gte=last_year)
    drugsLastYearTotalSum = DrugsIssuing.objects.filter(date_created__gte=last_year).aggregate(Sum('totalPrice')).get('totalPrice__sum')
    context = {'examsLastYear':examsLastYear, 'user':user, 'examsLastYearTotalSum':examsLastYearTotalSum,
               'drugsLastYear':drugsLastYear, 'drugsLastYearTotalSum':drugsLastYearTotalSum}
    html = template.render(context)
    pdf= render_to_pdf('lastYearReport.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Last Year Report"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def dateSearchedAdminReport(request):
    template = get_template('searchedDateReportAdmin.html')
    user = request.user
    try:
        date_search = request.GET.get('date_search')
    except:
        date_search = None
        
    if date_search:
        date_searched = date_search
        todaysDate = datetime.today()
        # print(date_searched)
        # print(todaysDate.date())
    # return render(request, 'test.html')
    
        # last_year = datetime.today() - timedelta(days=365)
    
    examsDateSearched = Medical_Exam.objects.filter(date_created__date=date_searched)
    examsDateSearchedTotalSum = Medical_Exam.objects.filter(date_created__date=date_searched).aggregate(Sum('exam__price')).get('exam__price__sum', 0.00)
    
    drugsDateSearched = DrugsIssuing.objects.filter(date_created__date=date_searched)
    drugsDateSearchedTotalSum = DrugsIssuing.objects.filter(date_created__date=date_searched).aggregate(Sum('totalPrice')).get('totalPrice__sum')
    context = {'examsDateSearched':examsDateSearched, 'user':user, 'examsDateSearchedTotalSum':examsDateSearchedTotalSum,
               'drugsDateSearched':drugsDateSearched, 'drugsDateSearchedTotalSum':drugsDateSearchedTotalSum, 'date_searched':date_searched}
    html = template.render(context)
    pdf= render_to_pdf('searchedDateReportAdmin.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Date Searched Report"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"



def lastWeekHosPDF(request):
    template = get_template('lastWeekReportHos.html')
    user = request.user
    hospital_agent = HospitalAgent.objects.get(user=user)
    hospital = Hospital.objects.get(agent=hospital_agent)
    last_week = datetime.today() - timedelta(days=7)
    
    examsLastWeek = Medical_Exam.objects.filter(hospital=hospital, date_created__gte=last_week)
    examsLastWeekTotalSum = Medical_Exam.objects.filter(hospital=hospital, date_created__gte=last_week).aggregate(Sum('exam__price')).get('exam__price__sum', 0.00)
    
    context = {'examsLastWeek':examsLastWeek, 'user':user, 'examsLastWeekTotalSum':examsLastWeekTotalSum,
               'user':user, 'hospital':hospital}
    html = template.render(context)
    pdf= render_to_pdf('lastWeekReportHos.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Last Week Report for %s" %(hospital)
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def lastMonthHosPDF(request):
    template = get_template('lastMonthReportHos.html')
    user = request.user
    hospital_agent = HospitalAgent.objects.get(user=user)
    hospital = Hospital.objects.get(agent=hospital_agent)
    last_month = datetime.today() - timedelta(days=30)
    
    examsLastMonth = Medical_Exam.objects.filter(hospital=hospital, date_created__gte=last_month)
    examsLastMonthTotalSum = Medical_Exam.objects.filter(hospital=hospital, date_created__gte=last_month).aggregate(Sum('exam__price')).get('exam__price__sum', 0.00)
    
    context = {'examsLastMonth':examsLastMonth, 'user':user, 'examsLastMonthTotalSum':examsLastMonthTotalSum,
               'user':user, 'hospital':hospital}
    html = template.render(context)
    pdf= render_to_pdf('lastMonthReportHos.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Last Month Report for %s" %(hospital)
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"


def lastYearHosPDF(request):
    template = get_template('lastYearReportHos.html')
    user = request.user
    hospital_agent = HospitalAgent.objects.get(user=user)
    hospital = Hospital.objects.get(agent=hospital_agent)
    last_year = datetime.today() - timedelta(days=365)
    
    examsLastYear = Medical_Exam.objects.filter(hospital=hospital, date_created__gte=last_year)
    examsLastYearTotalSum = Medical_Exam.objects.filter(hospital=hospital, date_created__gte=last_year).aggregate(Sum('exam__price')).get('exam__price__sum', 0.00)
    
    context = {'examsLastYear':examsLastYear, 'user':user, 'examsLastYearTotalSum':examsLastYearTotalSum,
               'user':user, 'hospital':hospital}
    html = template.render(context)
    pdf= render_to_pdf('lastYearReportHos.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Last Year Report for %s" %(hospital)
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def dateHosPDF(request):
    template = get_template('searchedDateReportHos.html')
    user = request.user
    hospital_agent = HospitalAgent.objects.get(user=user)
    hospital = Hospital.objects.get(agent=hospital_agent)
    
    try:
        date_search = request.GET.get('date_search')
    except:
        date_search = None
        
    if date_search:
        date_searched = date_search
        todaysDate = datetime.today()
        # print(date_searched)
        # print(todaysDate.date())
    # return render(request, 'test.html')
    
        # last_year = datetime.today() - timedelta(days=365)
        
        examsDateSearched = Medical_Exam.objects.filter(hospital=hospital, date_created__date=date_searched)
        examsDateSearchedTotalSum = Medical_Exam.objects.filter(hospital=hospital, date_created__date=date_searched).aggregate(Sum('exam__price')).get('exam__price__sum', 0.00)
        
        print(examsDateSearched)
        
        # return render(request, 'test.html')
        context = {'examsDateSearched':examsDateSearched, 'user':user, 'examsDateSearchedTotalSum':examsDateSearchedTotalSum,
                'user':user, 'hospital':hospital, 'date_searched':date_searched}
        html = template.render(context)
        pdf= render_to_pdf('searchedDateReportHos.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            file_name = "Date Searched Report for %s" %(hospital)
            content = "inline; filename='%s'" %(file_name)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(file_name)
            response['Content-Disposition'] = content
            return response
        return HttpResponse*"Not found"