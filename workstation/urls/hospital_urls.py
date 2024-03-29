from django.urls import path
from workstation.views.hospital_views import *

urlpatterns = [
    path('create', HospitalCreateView.as_view(), name='create_hospital'),
    path('list', hospitalList, name='hospital_list'),
    path('detail/<str:pk>', hospitalDetail, name='hospitalDetail'),
    path('delete/<str:id>', delete_hospital, name='delete_hospital'),
    path('update/<str:pk>', update_hospital, name='update_hospital'),
    # path('<str:id>/edit',hosAgentsViews.HospitalAgentUpdate.as_view(),name="hospitalAgent_edit"),
    # path('<str:id>/delete',hosAgentsViews.delete_hospitalAgent,name="hospitalAgent_delete"),
    # path('<str:id>/detail',hosAgentsViews.hospitalAgent_detail,name="hospitalAgent_detail"),
    
    path('pass/<int:pk>/', providePassToBeneficiary, name='pass'),
    path('provide_ordonance/<str:pk>', provide_ordonance, name='provide_ordonance'),
    path('ordonance/<str:pk>', print_ordonance, name='ordonance'),
    path('reportsHos', hospitalStatisticalReport, name='hospitalStatisticalReport'),
    path('history', benTreatmantHistory, name='history'),
    path('all_beneficiaries', reportAllBeneficiaries, name='all_beneficiaries'),
    path('hos_parmacies', hos_parmaciesPDF, name='hos_parmacies'),
    path('medecinesAllowed', medecinesAllowed, name='medecinesAllowed'),
    path('medical_exams/<str:pk>', provide_medical_exams, name='medical_exams'),
    
    path('comapare2MonthsHos', comapare2MonthsHos, name='comapare2MonthsHos'),
    path('addSuggestion/<str:pk>', addSuggestion, name='addSuggestion'),


]