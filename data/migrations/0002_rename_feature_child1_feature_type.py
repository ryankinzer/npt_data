# Generated by Django 4.0.5 on 2023-03-02 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='child1',
            old_name='feature',
            new_name='feature_type',
        ),
    ]
