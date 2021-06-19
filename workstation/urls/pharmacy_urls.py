from django.urls import path
from workstation.views.pharmacy_views import pharmacyList, PhamacyCreateView, pharmacyStatisticalReport, medecineProvision,print_ordonance_phar, saveDrugIssue, deliverMedecine

urlpatterns = [
    path('create', PhamacyCreateView.as_view(), name='create_pharmacy'),
    path('list', pharmacyList, name='pharmacy_list'),
    # path('<str:id>/edit',hosAgentsViews.HospitalAgentUpdate.as_view(),name="hospitalAgent_edit"),
    # path('<str:id>/delete',hosAgentsViews.delete_hospitalAgent,name="hospitalAgent_delete"),
    # path('<str:id>/detail',hosAgentsViews.hospitalAgent_detail,name="hospitalAgent_detail"),
    path('reports', pharmacyStatisticalReport, name='pharmacyStatisticalReport'),
    path('medecineProvision/<str:pk_ben>', medecineProvision, name='medecineProvision'),
    # path('deliverMedecine/<str:pk_ord>', deliverMedecine, name='deliverMedecine'),
    path('print_ordonance/<str:pk>', print_ordonance_phar, name='print_ordonance'),
    path('deliverMedecine/<str:pk>', deliverMedecine, name='deliverMedecine'),
    path('saveDrugIssue/<str:pk>', saveDrugIssue, name='saveDrugIssue')

]