# Generated by Django 5.0.2 on 2024-03-15 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_userreletion_userrelation_delete_mymodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserRelation',
            new_name='UserReletion',
        ),
    ]
