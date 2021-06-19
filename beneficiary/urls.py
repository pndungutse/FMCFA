from django.contrib import admin
from django.urls import path
from beneficiary import views

urlpatterns = [
    
    path('create', views.BeneficiaryCreateView.as_view(), name='create_beneficiary'),
    path('list', views.BeneficiaryListView.as_view(), name='list_beneficiary'),
    path('list_beneficiary', views.BeneficiaryListViewHospital.as_view(), name='list_beneficiary_hos'),
    path('list_beneficiary_phar', views.BeneficiaryListViewPharmacy.as_view(), name='list_beneficiary_phar'),
    path('view/<str:pk>', views.beneficiaryDetailView, name='detail_beneficiary'),
    path('beneficiaryDetail/<str:pk>', views.beneficiaryDetailViewPhar, name='beneficiaryDetailPhar'),
    path('beneficiaryDetailHos/<str:pk>', views.beneficiaryDetailViewHos, name='beneficiaryDetailHos'),
    path('<int:pk>/update', views.BeneficiaryUpdateView.as_view(), name='update_beneficiary'),
    path('<str:id>/delete',views.delete_beneficiary,name="beneficiary_delete"),
]
 