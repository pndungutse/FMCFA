from django.urls import path
from workers.views import pharmacistViews

urlpatterns = [
    # path('create', pharmacistViews.PharmacistCreateView.as_view(), name='create_pharmacist'),
    path('create', pharmacistViews.register_pharmacy_agent, name='create_pharmacist'),
    path('list', pharmacistViews.PharmacistList.as_view(), name='pharmacist_list'),
    path('<str:id>/edit',pharmacistViews.PharmacistUpdate.as_view(),name="pharmacist_edit"),
    path('<str:id>/delete',pharmacistViews.delete_pharmacist,name="pharmacist_delete"),
    path('<str:id>/detail',pharmacistViews.pharmacist_detail,name="pharmacist_detail"),

]

