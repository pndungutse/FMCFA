from django.contrib import admin
from django.urls import path, include
from accounts.views import render_dashboard, render_pharmacy_dashboard, viewSuggestions
from workstation.views.hospital_views import render_hospital_dashboard, adminReports
from drugs.views import exam_list, exam_create, examDetail, delete_exam, update_exam
from workers.views.hosAgentsViews import dateSearchedAdminReport, dateHosPDF, lastWeekAdminPDF, lastMonthAdminPDF, lastYearAdminPDF, lastWeekHosPDF, lastMonthHosPDF, lastYearHosPDF

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', admin.site.urls),
    path('dashboard/', render_dashboard, name='dashboard'),
    path('hos_dashboard/', render_hospital_dashboard, name='hos_dashboard'),
    path('phar_dashboard/', render_pharmacy_dashboard, name='phar_dashboard'),
    path('suggestions/', viewSuggestions, name='suggestions'),
    path('accounts/', include('accounts.urls')),
    path('beneficiary/', include('beneficiary.urls')),
    path('drug/', include('drugs.urls')),
    path('pharmacist/', include('workers.urls.pharmacist_urls')),
    path('hospitalAgent/', include('workers.urls.hosAgent_urls')),
    path('hospital/', include('workstation.urls.hospital_urls')),
    path('pharmacy/', include('workstation.urls.pharmacy_urls')),
    
    path('exam/list', exam_list, name='exam_list'),
    path('exam/create', exam_create, name='exam_create'),
    path('exam/update/<str:pk>', update_exam, name='update_exam'),
    path('exam/delete/<str:id>', delete_exam, name='delete_exam'),
    path('exam/detail/<str:pk>', examDetail, name='exam_detail'),
    
    path('last_week', lastWeekAdminPDF, name='last_week'),
    path('last_month', lastMonthAdminPDF, name='last_month'),
    path('last_year', lastYearAdminPDF, name='last_year'),
    path('dateSearched', dateSearchedAdminReport, name='dateSearched'),
    
    
    path('last_week_hos', lastWeekHosPDF, name='lastWeekHosPDF'),
    path('last_month_hos', lastMonthHosPDF, name='lastMonthHosPDF'),
    path('last_year_hos',lastYearHosPDF, name='lastYearHosPDF'),
    path('reports', adminReports, name='adminReports'),
    
    path('dateHosPDF', dateHosPDF, name='dateHosPDF'),
    
    
    
    
    
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
 