from django.contrib import admin
from django.urls import path, include
from accounts.views import render_dashboard, render_pharmacy_dashboard
from workstation.views.hospital_views import render_hospital_dashboard

urlpatterns = [
    path('', admin.site.urls),
    path('dashboard/', render_dashboard, name='dashboard'),
    path('hos_dashboard/', render_hospital_dashboard, name='hos_dashboard'),
    path('phar_dashboard/', render_pharmacy_dashboard, name='phar_dashboard'),
    path('accounts/', include('accounts.urls')),
    path('beneficiary/', include('beneficiary.urls')),
    path('drug/', include('drugs.urls')),
    path('pharmacist/', include('workers.urls.pharmacist_urls')),
    path('hospitalAgent/', include('workers.urls.hosAgent_urls')),
    path('hospital/', include('workstation.urls.hospital_urls')),
    path('pharmacy/', include('workstation.urls.pharmacy_urls')),
    
    
]
 