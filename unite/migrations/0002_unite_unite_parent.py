# Generated by Django 4.2.20 on 2025-04-23 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='unite',
            name='unite_parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sous_unites', to='unite.unite'),
        ),
    ]
