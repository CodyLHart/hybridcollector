from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('hybrids/', views.hybrids_index, name='index'),
    path('hybrids/<int:hybrid_id>/', views.hybrids_detail, name='detail'),
    path('hybrids/create/', views.HybridCreate.as_view(), name='hybrids_create'),
    path('hybrids/<int:pk>/update/', views.HybridUpdate.as_view(), name='hybrids_update'),
    path('hybrids/<int:pk>/delete/', views.HybridDelete.as_view(), name='hybrids_delete'),
    path('hybrids/<int:hybrid_id>/add_appointment/', views.add_appointment, name='add_appointment'),
    path('hybrids/<int:hybrid_id>/add_photo/', views.add_photo, name='add_photo'),
    path('hybrids/<int:hybrid_id>/assoc_vest/<int:vest_id>/', views.assoc_vest, name='assoc_vest'),
    path('hybrids/<int:hybrid_id>/unassoc_vest/<int:vest_id>/', views.unassoc_vest, name='unassoc_vest'),
    path('vests/', views.VestList.as_view(), name='vests_index'),
    path('vests/<int:pk>/', views.VestDetail.as_view(), name='vests_detail'),
    path('vests/create/', views.VestCreate.as_view(), name='vests_create'),
    path('vests/<int:pk>/update/', views.VestUpdate.as_view(), name='vests_update'),
    path('vests/<int:pk>/delete/', views.VestDelete.as_view(), name='vests_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]

