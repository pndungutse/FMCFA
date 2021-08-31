from workstation.models.hospital import Drug, DrugsIssuing, Suggestion
from beneficiary.models import Beneficiary
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from accounts.decolator import unauthenticated_user, allowed_users
from django.contrib.auth.views import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from workers.models.hosAgent import HospitalAgent
from workers.models.pharmacist import Pharmacist
from workstation.models.hospital import Hospital, Pass
from workstation.models.pharmacy import Pharmacy
import datetime
from django.db.models import Sum



# Create your views here.
def render_dashboard(request):
    no_hospitals = Hospital.objects.all().count()
    no_pharmacies = Pharmacy.objects.all().count()
    no_beneficiaries = Beneficiary.objects.all().count()
    no_drugs = Drug.objects.all().count()
    year =datetime.datetime.now().year
    
    january = Pass.objects.filter(date_created__year__gte=year, date_created__month=1).count()
    february = Pass.objects.filter(date_created__year__gte=year, date_created__month=2).count()
    march = Pass.objects.filter(date_created__year__gte=year, date_created__month=3).count()
    april = Pass.objects.filter(date_created__year__gte=year, date_created__month=4).count()
    may = Pass.objects.filter(date_created__year__gte=year, date_created__month=5).count()
    june = Pass.objects.filter(date_created__year__gte=year, date_created__month=6).count()
    july = Pass.objects.filter(date_created__year__gte=year, date_created__month=7).count()
    august = Pass.objects.filter(date_created__year__gte=year, date_created__month=8).count()
    september = Pass.objects.filter(date_created__year__gte=year, date_created__month=9).count()
    october = Pass.objects.filter(date_created__year__gte=year, date_created__month=10).count()
    november = Pass.objects.filter(date_created__year__gte=year, date_created__month=11).count()
    december = Pass.objects.filter(date_created__year__gte=year, date_created__month=12).count()
    
    context = {'no_hospitals':no_hospitals, 'no_pharmacies':no_pharmacies, 'no_beneficiaries':no_beneficiaries, 'no_drugs':no_drugs, 
               'january':january, 'february':february, 'march':march, 'april':april, 'may':may,'june':june, 
               'july':july, 'august':august, 'september':september, 'october':october, 'november':november, 'december':december}
    return render(request, 'main_dashboard.html', context)



def render_pharmacy_dashboard(request):
    user = request.user
    pharmacist = Pharmacist.objects.get(user=user)
    pharmacy = Pharmacy.objects.get(agent=pharmacist)
    year = datetime.datetime.now().year
    
    january = DrugsIssuing.objects.filter(date_created__year__gte=year, date_created__month=1).aggregate(Sum('totalPrice'))
    february = DrugsIssuing.objects.filter(date_created__year__gte=year, date_created__month=2).aggregate(Sum('totalPrice'))
    march = DrugsIssuing.objects.filter(date_created__year__gte=year, date_created__month=3).aggregate(Sum('totalPrice'))
    april = DrugsIssuing.objects.filter(date_created__year__gte=year, date_created__month=4).aggregate(Sum('totalPrice'))
    may = DrugsIssuing.objects.filter(date_created__year__gte=year, date_created__month=5).aggregate(Sum('totalPrice'))
    june = DrugsIssuing.objects.filter(date_created__year__gte=year, date_created__month=6).aggregate(Sum('totalPrice'))
    july = DrugsIssuing.objects.filter(date_created__year__gte=year, date_created__month=7).aggregate(Sum('totalPrice'))
    august = DrugsIssuing.objects.filter(date_created__year__gte=year, date_created__month=8).aggregate(Sum('totalPrice'))
    september = DrugsIssuing.objects.filter(date_created__year__gte=year, date_created__month=9).aggregate(Sum('totalPrice'))
    october = DrugsIssuing.objects.filter(date_created__year__gte=year, date_created__month=10).aggregate(Sum('totalPrice'))
    november = DrugsIssuing.objects.filter(date_created__year__gte=year, date_created__month=11).aggregate(Sum('totalPrice'))
    december = DrugsIssuing.objects.filter(date_created__year__gte=year, date_created__month=12).aggregate(Sum('totalPrice'))
    
    context = {'pharmacy':pharmacy, 
               'january':january, 'february':february, 'march':march, 'april':april, 'may':may,'june':june, 
               'july':july, 'august':august, 'september':september, 'october':october, 'november':november, 'december':december
               }
    return render(request, 'workers/pharmacist/pharmacyDashboard.html', context)

@login_required(login_url='/accounts/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'You have successfully changed the password')
            return redirect('profile')
        else:
            messages.error(request, 'Error in changing password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {
        'form': form
    })



def render_404(request, exception):
    return render(request, 'accounts/error-404.html')


# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             # log the user in
#             user = form.get_user()
#             login(request, user)
#             if 'next' in request.POST:
#                 return redirect(request.POST.get('next'))
#             else:
#                return redirect('dashboard')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'accounts/login.html', { 'form': form })


@unauthenticated_user
def loginOrg(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log the user in
            user = form.get_user()
            login(request, user)
            if HospitalAgent.objects.filter(user=user):
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('hos_dashboard')
            elif Pharmacist.objects.filter(user=user):
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('phar_dashboard')
            elif user.is_superuser:
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    
def viewSuggestions(request):
    suggestions = Suggestion.objects.all()
    context = {'suggestions': suggestions}
    return render(request, 'suggestions.html', context)
    