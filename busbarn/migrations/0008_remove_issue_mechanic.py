# Generated by Django 2.1.7 on 2019-02-12 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('busbarn', '0007_transfer_mechanics'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='mechanic',
        ),
    ]
