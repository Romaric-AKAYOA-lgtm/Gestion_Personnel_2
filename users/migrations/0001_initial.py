# Generated by Django 4.2.20 on 2025-04-17 16:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tnm', models.CharField(max_length=50)),
                ('tpm', models.CharField(blank=True, max_length=50, null=True)),
                ('tsx', models.CharField(choices=[('Masculin', 'Masculin'), ('Feminin', 'Féminin')], default='Masculin', max_length=10)),
                ('dns', models.DateField()),
                ('date_retraite', models.DateField(blank=True, null=True)),
                ('tlns', models.CharField(blank=True, max_length=50, null=True)),
                ('tads', models.CharField(blank=True, max_length=50, null=True)),
                ('teml', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('tphne', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('dsb', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('ddf', models.DateField(blank=True, null=True)),
                ('tstt', models.CharField(blank=True, max_length=50, null=True)),
                ('ttvst', models.CharField(max_length=50)),
                ('img', models.ImageField(blank=True, null=True, upload_to='user_images/')),
            ],
        ),
    ]
