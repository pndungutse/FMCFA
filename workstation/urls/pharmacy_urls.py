from django.urls import path
from workstation.views.pharmacy_views import lastYearPharPDF,lastMonthPharPDF,lastWeekPharPDF,update_pharmacy,delete_pharmacy,pharmacyDetail,pharmacyList, PhamacyCreateView, pharmacyStatisticalReport, medecineProvision,print_ordonance_phar, saveDrugIssue, deliverMedecine

urlpatterns = [
    path('create', PhamacyCreateView.as_view(), name='create_pharmacy'),
    path('list', pharmacyList, name='pharmacy_list'),
    path('detail/<str:pk>', pharmacyDetail, name='pharmacy_detail'),
    path('delete/<str:id>', delete_pharmacy, name='pharmacy_delete'),
    path('update/<str:pk>', update_pharmacy, name='update_pharmacy'),
    # path('<str:id>/edit',hosAgentsViews.HospitalAgentUpdate.as_view(),name="hospitalAgent_edit"),
    # path('<str:id>/delete',hosAgentsViews.delete_hospitalAgent,name="hospitalAgent_delete"),
    # path('<str:id>/detail',hosAgentsViews.hospitalAgent_detail,name="hospitalAgent_detail"),
    path('reports', pharmacyStatisticalReport, name='pharmacyStatisticalReport'),
    path('medecineProvision/<str:pk_ben>', medecineProvision, name='medecineProvision'),
    # path('deliverMedecine/<str:pk_ord>', deliverMedecine, name='deliverMedecine'),
    path('print_ordonance/<str:pk>', print_ordonance_phar, name='print_ordonance'),
    path('deliverMedecine/<str:pk>', deliverMedecine, name='deliverMedecine'),
    path('saveDrugIssue/<str:pk>', saveDrugIssue, name='saveDrugIssue'),
    
    path('last_week_phar', lastWeekPharPDF, name='lastWeekPharPDF'),
    path('last_month_phar', lastMonthPharPDF, name='lastMonthPharPDF'),
    path('last_year_phar', lastYearPharPDF, name='lastYearPharPDF'),

]