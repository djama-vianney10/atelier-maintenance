from django.db import models

# Create your models here.
class Agent(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    adresse = models.CharField(max_length=100)
    grade = models.CharField(max_length=50)
    service = models.CharField(max_length=50)

    def __str__(self):
        return self.nom

class Appareil(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='appareils')
    nom = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    marque = models.CharField(max_length=100)
    etat = models.CharField(max_length=100, choices=[
    ('en_reparation', 'En reparation'),
    ('en_panne', 'En panne'),
    ('repare', 'Réparé'),
], default='En reparation')

    def __str__(self):
        return f"{self.nom} ({self.modele} - {self.marque})"

class Technicien(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    statut = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    condition = models.CharField(max_length=50, choices=[
    ('disponible', 'Disponible'),
    ('occupe', 'Occupé'),
], default='disponible')

    def __str__(self):
        return self.nom

class Intervention(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='interventions')
    appareils = models.ManyToManyField(Appareil, related_name='interventions')
    techniciens = models.ManyToManyField(Technicien, related_name='interventions')
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    SITUATION_CHOICES = [
    ('en cours', 'En cours'),
    ('terminée', 'Terminée'),
]
    situation = models.CharField(max_length=20, choices=SITUATION_CHOICES, default='en cours', verbose_name='Situation')

    def __str__(self):
        return f"Intervention #{self.id} - {self.date_debut.strftime('%d-%m-%Y')}"

class Tache(models.Model):
    intervention = models.ForeignKey(Intervention, on_delete=models.CASCADE, related_name='taches')
    description = models.TextField()

    def __str__(self):
        return self.description

class Diagnostic(models.Model):
    description = models.TextField()
    techniciens = models.ManyToManyField(Technicien, related_name='diagnostics')

    def __str__(self):
        return f"Diagnostic #{self.id} - {self.description}"
