from django.contrib import admin
from .models import Agent, Appareil, Technicien, Intervention, Tache, Diagnostic

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'adresse', 'grade', 'service')

@admin.register(Appareil)
class AppareilAdmin(admin.ModelAdmin):
    list_display = ('nom', 'modele', 'agent', 'marque')
    list_filter = ('agent',)

@admin.register(Technicien)
class TechnicienAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'statut', 'telephone')

@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_debut', 'date_fin')
    filter_horizontal = ('appareils', 'techniciens')

@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ('description', 'intervention')

@admin.register(Diagnostic)
class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    filter_horizontal = ('techniciens',)
