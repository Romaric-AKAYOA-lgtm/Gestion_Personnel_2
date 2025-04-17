# Generated by Django 4.2.20 on 2025-04-17 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('localisation', models.CharField(max_length=255)),
                ('logo', models.ImageField(upload_to='logos/')),
                ('devise', models.CharField(max_length=50)),
                ('pays', models.CharField(max_length=50)),
                ('devise_pays', models.CharField(max_length=50)),
                ('drapeau', models.ImageField(upload_to='drapeaux/')),
            ],
        ),
    ]
