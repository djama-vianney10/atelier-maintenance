# Generated by Django 5.1.5 on 2025-07-08 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atelier', '0002_appareil_etat_intervention_situation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intervention',
            name='situation',
            field=models.CharField(choices=[('en cours', 'En cours'), ('terminée', 'Terminée')], default='en cours', max_length=20),
        ),
    ]
