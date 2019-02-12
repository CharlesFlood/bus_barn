# Generated by Django 2.1.7 on 2019-02-12 02:27

from django.db import migrations



def linkMechanics(apps, schema_editor):
    Issue = apps.get_model('busbarn', 'Issue')
    Mechanic = apps.get_model('busbarn', 'Mechanic')
    for issue in Issue.objects.all():
        mechanic, created = Mechanic.objects.get_or_create(name=issue.mechanic)
        issue.mechanic_link = mechanic
        issue.save()

def unlinkMechanics(apps, schema_editor):
    Issue = apps.get_model('busbarn', 'Issue')
    Mechanic = apps.get_model('busbarn', 'Mechanic')
    for issue in Issue.objects.all():
        issue.mechanic_link = None
        issue.save()

class Migration(migrations.Migration):

    dependencies = [
        ('busbarn', '0006_auto_20190212_0223'),
    ]

    operations = [
        migrations.RunPython(linkMechanics, unlinkMechanics),
    ]
