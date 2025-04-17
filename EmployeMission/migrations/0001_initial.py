# Generated by Django 4.2.20 on 2025-04-17 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Employe', '0001_initial'),
        ('mission', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CLEmployeMission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut', models.CharField(choices=[('Collaborateur', 'Collaborateur'), ('Chef de mission', 'Chef de mission')], max_length=20)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employe.clemploye')),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mission.clmission')),
            ],
        ),
    ]
