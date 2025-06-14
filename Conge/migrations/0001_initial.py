# Generated by Django 4.2.20 on 2025-05-26 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Employe', '0001_initial'),
        ('TypeConge', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CLConge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut_previsionnel', models.DateField(blank=True, help_text='Date prévisionnelle de début du congé', null=True)),
                ('date_retour_previsionnel', models.DateField(blank=True, help_text='Date prévisionnelle de retour du congé', null=True)),
                ('date_retour_definitif', models.DateField(blank=True, help_text='Date définitive de retour du congé', null=True)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employe.clemploye')),
                ('typeconge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TypeConge.cltypeconge')),
            ],
        ),
    ]
