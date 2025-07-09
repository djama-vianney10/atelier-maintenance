from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Appareil, Agent, Intervention, Technicien, Diagnostic, Tache

class AppareilForm(forms.ModelForm):
    class Meta:
        model = Appareil
        fields = ['nom', 'modele', 'marque', 'agent']

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['nom', 'prenom', 'adresse', 'grade', 'service']

class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = ['agent', 'appareils', 'techniciens', 'date_debut', 'date_fin', 'description', 'situation']
        widgets = {
            'situation': forms.RadioSelect(),  # Rend le champ en boutons radio
        }

class TechnicienForm(forms.ModelForm):
    class Meta:
        model = Technicien
        fields = ['nom', 'prenom', 'statut', 'telephone']

class DiagnosticForm(forms.ModelForm):
    class Meta:
        model = Diagnostic
        fields = ['techniciens', 'description']

class TacheForm(forms.ModelForm):
    class Meta:
        model = Tache
        fields = ['intervention', 'description']

class FiltreInterventionForm(forms.Form):
    date_debut = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_fin = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    technicien = forms.ModelChoiceField(queryset=Technicien.objects.all(), required=False)
    situation = forms.ChoiceField(choices=[('', 'Toutes'), ('terminee', 'Terminée'), ('en_cours', 'En cours')], required=False)


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adresse e-mail")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']