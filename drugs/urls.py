from django.contrib import admin
from django.urls import path
from drugs import views

urlpatterns = [
    # path('create', views.DrugCreateView.as_view(), name='create_drug'),
    path('list', views.drug_list, name='list_drug'),
    path('create', views.drug_create, name='drug_create'),
    path('update/<str:pk>', views.update_drug, name='update_drug'),
    path('detail/<str:pk>', views.drugDetail, name='drug_detail'),
    path('delete/<str:id>', views.delete_drug, name='delete_drug'),
    path('<int:pk>/view', views.DrugDetailView.as_view(), name='detail_drug'),
    # path('<int:pk>/update', views.DrugUpdateView.as_view(), name='update_drug'),
]
  