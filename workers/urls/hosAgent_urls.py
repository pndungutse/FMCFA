from django.urls import path
from workers.views import hosAgentsViews

urlpatterns = [
    # path('create', hosAgentsViews.HospitalAgentCreateView.as_view(), name='create_hospitalAgent'),
    path('create', hosAgentsViews.register_hospital_agent, name='create_hospitalAgent'),
    path('list', hosAgentsViews.HospitalAgentList.as_view(), name='hospitalAgent_list'),
    path('<str:id>/edit',hosAgentsViews.HospitalAgentUpdate.as_view(),name="hospitalAgent_edit"),
    path('<str:id>/delete',hosAgentsViews.delete_hospitalAgent,name="hospitalAgent_delete"),
    path('<str:id>/detail',hosAgentsViews.hospitalAgent_detail,name="hospitalAgent_detail"),

]

