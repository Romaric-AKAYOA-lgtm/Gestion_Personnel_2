# Generated by Django 4.2.20 on 2025-05-03 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Conge', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clconge',
            name='employe_signature',
        ),
    ]
