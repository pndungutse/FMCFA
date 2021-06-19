from django.contrib import admin
from django.urls import path
from drugs import views

urlpatterns = [
    path('create', views.DrugCreateView.as_view(), name='create_drug'),
    path('list', views.DrugListView.as_view(), name='list_drug'),
    path('<int:pk>/view', views.DrugDetailView.as_view(), name='detail_drug'),
    path('<int:pk>/update', views.DrugUpdateView.as_view(), name='update_drug'),
]
  