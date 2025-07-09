from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib import messages
from .models import Appareil, Agent, Intervention, Technicien, Diagnostic, Tache
from .forms import AppareilForm, AgentForm, InterventionForm, TechnicienForm, DiagnosticForm, TacheForm, FiltreInterventionForm, CustomUserCreationForm

# Create your views here.

#Create formulaire register
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion automatique après inscription
            messages.success(request, "Inscription réussie. Bienvenue !")
            return redirect('dashboard')  # Redirection vers le tableau de bord
        else:
            messages.error(request, "Erreur lors de l'inscription.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'atelier/register.html', {'form': form})

#Create Dashboard
@login_required
def dashboard(request):
    interventions = Intervention.objects.select_related('agent').prefetch_related('techniciens', 'appareils').order_by('-date_debut')
    
    form = FiltreInterventionForm(request.GET or None)

    if form.is_valid():
        if form.cleaned_data['date_debut']:
            interventions = interventions.filter(date_debut__gte=form.cleaned_data['date_debut'])

        if form.cleaned_data['date_fin']:
            interventions = interventions.filter(date_debut__lte=form.cleaned_data['date_fin'])

        if form.cleaned_data['technicien']:
            interventions = interventions.filter(techniciens=form.cleaned_data['technicien'])

        situation = form.cleaned_data['situation']
        if situation == 'terminee':
            interventions = interventions.filter(situation=True)
        elif situation == 'en_cours':
            interventions = interventions.filter(situation=False)

    # Statistiques
    total_interventions = Intervention.objects.count()
    interventions_terminees = Intervention.objects.filter(situation='terminée').count()
    interventions_en_cours = total_interventions - interventions_terminees

    appareils_repares = Appareil.objects.filter(etat='réparé').count()
    appareils_pannes = Appareil.objects.exclude(etat='réparé').count()

    techniciens_disponibles = Technicien.objects.filter(condition='disponible').count()
    techniciens_occupes = Technicien.objects.filter(condition='occupé').count()

    context = {
        'total_interventions': total_interventions,
        'interventions_terminees': interventions_terminees,
        'interventions_en_cours': interventions_en_cours,
        'appareils_repares': appareils_repares,
        'appareils_pannes': appareils_pannes,
        'techniciens_disponibles': techniciens_disponibles,
        'techniciens_occupes': techniciens_occupes,
        'interventions': interventions,
        'form': form
    }

    return render(request, 'atelier/dashboard.html', context)

# Lister tous les appareils
@login_required
def appareil_list(request):
    appareils = Appareil.objects.all()
    return render(request, 'atelier/appareil_list.html', {'appareils': appareils})

# Ajouter un appareil
def appareil_create(request):
    if request.method == 'POST':
        form = AppareilForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Appareil ajouté avec succès.")
            return redirect('appareil_list')
        else:
            messages.error(request, "Erreur lors de l'ajout.")
    else:
        form = AppareilForm()
    return render(request, 'atelier/appareil_form.html', {'form': form})

# Modifier un appareil
def appareil_update(request, pk):
    appareil = get_object_or_404(Appareil, pk=pk)
    if request.method == 'POST':
        form = AppareilForm(request.POST, instance=appareil)
        if form.is_valid():
            form.save()
            messages.success(request, "Appareil modifié avec succès.")
            return redirect('appareil_list')
        else:
            messages.error(request, "Erreur lors de la modification.")
    else:
        form = AppareilForm(instance=appareil)
    return render(request, 'atelier/appareil_form.html', {'form': form})

# Supprimer un appareil
def appareil_delete(request, pk):
    appareil = get_object_or_404(Appareil, pk=pk)
    if request.method == 'POST':
        appareil.delete()
        messages.success(request, "Appareil supprimé avec succès.")
        return redirect('appareil_list')
    return render(request, 'atelier/appareil_confirm_delete.html', {'appareil': appareil})


# CREATE AGENT
def agent_create(request):
    if request.method == 'POST':
        form = AgentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Agent ajouté avec succès.")
            return redirect('agent_list')
    else:
        form = AgentForm()
    return render(request, 'atelier/agent_form.html', {'form': form})


# READ (LISTE)
@login_required
def agent_list(request):
    agents = Agent.objects.all()
    return render(request, 'atelier/agent_list.html', {'agents': agents})


# READ (DÉTAIL)
def agent_detail(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    return render(request, 'atelier/agent_detail.html', {'agent': agent})


# UPDATE
def agent_update(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    if request.method == 'POST':
        form = AgentForm(request.POST, instance=agent)
        if form.is_valid():
            form.save()
            messages.success(request, "Agent modifié avec succès.")
            return redirect('agent_detail', pk=pk)
    else:
        form = AgentForm(instance=agent)
    return render(request, 'atelier/agent_form.html', {'form': form})

# DELETE
def agent_delete(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    if request.method == 'POST':
        agent.delete()
        messages.success(request, "Agent supprimé avec succès.")
        return redirect('agent_list')
    return render(request, 'atelier/agent_confirm_delete.html', {'agent': agent})


#List INTERVENTION
@login_required
def intervention_list(request):
    interventions = Intervention.objects.all()
    return render(request, 'atelier/intervention_list.html', {'interventions': interventions})

#CREATE intervention
def intervention_create(request):
    if request.method == 'POST':
        form = InterventionForm(request.POST)
        if form.is_valid():
            intervention = form.save(commit=False)
            intervention.save()
            form.save_m2m()

            # 🔁 Mettre à jour l'état des appareils si intervention est terminée
            if intervention.situation== 'terminée':
                for appareil in intervention.appareils.all():
                    appareil.etat = 'réparé'
                    appareil.save()

            # 🔁 Mettre à jour le statut des techniciens
            for technicien in intervention.techniciens.all():
                update_condition_technicien(technicien)

            messages.success(request, "Intervention ajoutée avec succès.")
            return redirect('intervention_list')
        else:
            messages.error(request, "Erreur lors de l'ajout de l'intervention.")
    else:
        form = InterventionForm()

    return render(request, 'atelier/intervention_form.html', {'form': form})

#UPDATE intervention
def intervention_update(request, pk):
    intervention = get_object_or_404(Intervention, pk=pk)

    if request.method == 'POST':
        form = InterventionForm(request.POST, instance=intervention)
        if form.is_valid():
            intervention = form.save(commit=False)
            intervention.save()
            form.save_m2m()  # Maintenant les techniciens sont bien enregistrés

            # 🔁 Mettre à jour l'état des appareils si intervention terminée
            if intervention.situation == 'terminée':
                for appareil in intervention.appareils.all():
                    appareil.etat = 'réparé'
                    appareil.save()

            # 🔁 Mettre à jour le statut des techniciens
            for technicien in intervention.techniciens.all():
                update_condition_technicien(technicien)

            messages.success(request, "Intervention modifiée avec succès.")
            return redirect('intervention_list')
        else:
            messages.error(request, "Erreur lors de la modification de l'intervention.")
    else:
        form = InterventionForm(instance=intervention)

    return render(request, 'atelier/intervention_form.html', {'form': form})

#DELETE intervention
def intervention_delete(request, pk):
    intervention = get_object_or_404(Intervention, pk=pk)
    if request.method == 'POST':
        intervention.delete()
        messages.success(request, "Intervention supprimée avec succès.")
        return redirect('intervention_list')

    return render(request, 'atelier/intervention_confirm_delete.html', {'intervention': intervention})




def update_condition_technicien(technicien):
     # Est-ce qu’il a encore des interventions "en cours" ?
    en_cours = technicien.interventions.filter(situation='en cours').exists()
    technicien.condition = 'occupé' if en_cours else 'disponible'
    technicien.save()


#lister techniciens
@login_required
def technicien_list(request):
    techniciens = Technicien.objects.all()
    return render(request, 'atelier/technicien_list.html', {'techniciens': techniciens})

#CREATE technicien
def technicien_create(request):
    if request.method == 'POST':
        form = TechnicienForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Technicien ajouté avec succès.")
            return redirect('technicien_list')
        else:
            messages.error(request, "Erreur lors de l'ajout du technicien.")
    else:
        form = TechnicienForm()
    return render(request, 'atelier/technicien_form.html', {'form': form})

#UPDATE technicien
def technicien_update(request, pk):
    technicien = get_object_or_404(Technicien, pk=pk)
    if request.method == 'POST':
        form = TechnicienForm(request.POST, instance=technicien)
        if form.is_valid():
            form.save()
            messages.success(request, "Technicien modifié avec succès.")
            return redirect('technicien_list')
        else:
            messages.error(request, "Erreur lors de la modification.")
    else:
        form = TechnicienForm(instance=technicien)
    return render(request, 'atelier/technicien_form.html', {'form': form})

#DELETE technicien
def technicien_delete(request, pk):
    technicien = get_object_or_404(Technicien, pk=pk)
    if request.method == 'POST':
        technicien.delete()
        messages.success(request, "Technicien supprimé avec succès.")
        return redirect('technicien_list')
    return render(request, 'atelier/technicien_confirm_delete.html', {'technicien': technicien})

#list diagnostic
def diagnostic_list(request):
    diagnostics = Diagnostic.objects.all()
    return render(request, 'atelier/diagnostic_list.html', {'diagnostics': diagnostics})

#CREATE diagnostic
def diagnostic_create(request):
    if request.method == 'POST':
        form = DiagnosticForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Diagnostic ajouté avec succès.")
            return redirect('diagnostic_list')
        else:
            messages.error(request, "Erreur lors de l'ajout.")
    else:
        form = DiagnosticForm()
    return render(request, 'atelier/diagnostic_form.html', {'form': form})

#UPDATE diagnostic
def diagnostic_update(request, pk):
    diagnostic = get_object_or_404(Diagnostic, pk=pk)
    if request.method == 'POST':
        form = DiagnosticForm(request.POST, instance=diagnostic)
        if form.is_valid():
            form.save()
            messages.success(request, "Diagnostic modifié avec succès.")
            return redirect('diagnostic_list')
        else:
            messages.error(request, "Erreur lors de la modification.")
    else:
        form = DiagnosticForm(instance=diagnostic)
    return render(request, 'atelier/diagnostic_form.html', {'form': form})

#DELETE diagnostic
def diagnostic_delete(request, pk):
    diagnostic = get_object_or_404(Diagnostic, pk=pk)
    if request.method == 'POST':
        diagnostic.delete()
        messages.success(request, "Diagnostic supprimé avec succès.")
        return redirect('diagnostic_list')
    return render(request, 'atelier/diagnostic_confirm_delete.html', {'diagnostic': diagnostic})

# List Taches
def tache_list(request):
    taches = Tache.objects.all()
    return render(request, 'atelier/tache_list.html', {'taches': taches})

# Create Tache
def tache_create(request):
    if request.method == 'POST':
        form = TacheForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tâche ajoutée avec succès.")
            return redirect('tache_list')
        else:
            messages.error(request, "Erreur lors de l'ajout.")
    else:
        form = TacheForm()
    return render(request, 'atelier/tache_form.html', {'form': form})

# Update Tache
def tache_update(request, pk):
    tache = get_object_or_404(Tache, pk=pk)
    if request.method == 'POST':
        form = TacheForm(request.POST, instance=tache)
        if form.is_valid():
            form.save()
            messages.success(request, "Tâche modifiée avec succès.")
            return redirect('tache_list')
        else:
            messages.error(request, "Erreur lors de la modification.")
    else:
        form = TacheForm(instance=tache)
    return render(request, 'atelier/tache_form.html', {'form': form})

# delete Tache
def tache_delete(request, pk):
    tache = get_object_or_404(Tache, pk=pk)
    if request.method == 'POST':
        tache.delete()
        messages.success(request, "Tâche supprimée avec succès.")
        return redirect('tache_list')
    return render(request, 'atelier/tache_confirm_delete.html', {'tache': tache})