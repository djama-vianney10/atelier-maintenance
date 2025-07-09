from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='atelier/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
     # Agent
    path('appareil/', views.appareil_list, name='appareil_list'),
    path('appareil/create/', views.appareil_create, name='appareil_create'),
    path('appareil/update/<int:pk>/', views.appareil_update, name='appareil_update'),
    path('appareil/delete/<int:pk>/', views.appareil_delete, name='appareil_delete'),

     # Appareil
    path('agent/', views.agent_list, name='agent_list'),
    path('agent/ajouter/', views.agent_create, name='agent_create'),
    path('agent/modifier/<int:pk>/', views.agent_update, name='agent_update'),
    path('agent/supprimer/<int:pk>/', views.agent_delete, name='agent_delete'),

    # Intervention
     path('intervention/', views.intervention_list, name='intervention_list'),
    path('intervention/ajouter/', views.intervention_create, name='intervention_create'),
    path('intervention/modifier/<int:pk>/', views.intervention_update, name='intervention_update'),
    path('intervention/supprimer/<int:pk>/', views.intervention_delete, name='intervention_delete'),

    # Technicien
    path('technicien/', views.technicien_list, name='technicien_list'),
    path('technicien/add/', views.technicien_create, name='technicien_create'),
    path('technicien/<int:pk>/edit/', views.technicien_update, name='technicien_update'),
    path('technicien/<int:pk>/delete/', views.technicien_delete, name='technicien_delete'),

    # Diagnostic
    path('diagnostic/', views.diagnostic_list, name='diagnostic_list'),
    path('diagnostic/add/', views.diagnostic_create, name='diagnostic_create'),
    path('diagnostic/<int:pk>/edit/', views.diagnostic_update, name='diagnostic_update'),
    path('diagnostic/<int:pk>/delete/', views.diagnostic_delete, name='diagnostic_delete'),

    # Tache
    path('tache/', views.tache_list, name='tache_list'),
    path('tache/add/', views.tache_create, name='tache_create'),
    path('tache/<int:pk>/edit/', views.tache_update, name='tache_update'),
    path('tache/<int:pk>/delete/', views.tache_delete, name='tache_delete'),
]