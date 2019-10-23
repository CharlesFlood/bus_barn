# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.timezone import now
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime


# Create your views here.
from .models import Vehicle, Issue, Mechanic
from .forms import IssueForm, MechanicForm

def index(request):
    return HttpResponseRedirect(reverse('busbarn:issue_list'))

def vehicle_list(request):
    vehicle_list = Vehicle.objects.all()
    context = {'vehicle_list': vehicle_list}
    return render(request, 'busbarn/vehicle_list.html', context)

def vehicle_detail(request, vehicle_id):
    # For this we need the vehicle detail and all associated 
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    issues = Issue.objects.filter(vehicle_id=vehicle_id)
    return render(request, 'busbarn/vehicle_detail.html', {'vehicle': vehicle, 'issues': issues })

def vehicle_basic_edit(request, vehicle_id):
    # currently do nothing
    return HttpResponse("Adding and editing vehicles can only be done through the admin interface.")

def mechanic_list(request):
    mechanic_list = Mechanic.objects.filter(active=True).order_by('name')
    #mechanic_list = Mechanic.objects.order_by('name')
    context = {'mechanic_list': mechanic_list}
    return render(request, 'busbarn/mechanic_list.html', context)

def mechanic_add(request):
    # TODO: implement using issue add as a template
    if request.method == "POST":
        form = MechanicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('busbarn:mechanic_list'))
    else:
        form = MechanicForm()
        return render(request, 'busbarn/mechanic_add.html', {'form': form})

def mechanic_update_status(request, mechanic_id, status):
    mechanic = get_object_or_404(Mechanic, id=mechanic_id)
    if status=="1":
        print("activating")
        mechanic.active = True
    else:
        print("deactivating")
        mechanic.active = False
    mechanic.save()
    return HttpResponseRedirect(reverse('busbarn:mechanic_list'))

def mechanic_edit(request, mechanic_id):
    instance = get_object_or_404(Mechanic, id=mechanic_id)
    form = MechanicForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        instance.save()
        return HttpResponseRedirect(reverse('busbarn:mechanic_list'))
    return render(request, 'busbarn/mechanic_edit.html', {'form': form, 'mechanic': instance})

def issue_list(request):
    issue_list = Issue.objects.filter(date_completed__isnull=True).filter(deleted=False).order_by('vehicle__vehicle_name')
    context = {'issue_list': issue_list}
    return render(request, 'busbarn/issue_list.html', context)
def issue_fixed(request):
    issue_list = Issue.objects.filter(date_completed__isnull=False).order_by('vehicle__vehicle_name')
    context = {'issue_list': issue_list}
    return render(request, 'busbarn/issue_fixed.html', context)


def issue_detail(request, issue_id):
    issue = Issue.objects.get(pk=issue_id)
    return render(request, 'busbarn/issue_detail.html', {'issue': issue})

def issue_edit(request, issue_id):
    instance = get_object_or_404(Issue, id=issue_id)
    form = IssueForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        form.cleaned_data['last_updated'] = now()
        if not form.cleaned_data['repair'] == "":
            instance.date_completed = now()
            instance.save()
        return HttpResponseRedirect(reverse('busbarn:issue_list'))
    return render(request, 'busbarn/issue_edit.html', {'form': form, 'issue': instance})

def issue_add(request, bus_id=None):
    if request.method == "POST":
        form = IssueForm(request.POST)
        if form.is_valid():
            form.cleaned_data['date_noted'] = now()
            #form.cleaned_data['last_updated'] = now()
            form.save()
            return HttpResponseRedirect(reverse('busbarn:issue_list'))
    else:
        if bus_id:
            form = IssueForm({'date_noted': now(), 'vehicle': bus_id})
        else:
            form = IssueForm({'date_noted': now()})
        #form.fields['date_noted'].disabled = True
        return render(request, 'busbarn/issue_add.html', {'form': form})

def issue_delete(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    issue.last_updated = now()
    issue.deleted = True
    issue.save()
    return HttpResponseRedirect(reverse("busbarn:issue_list"))
    
def issue_print(request):
    issue_list = Issue.objects.filter(date_completed__isnull=True).filter(deleted=False).order_by('vehicle__vehicle_name')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="printout.pdf"'
    now = datetime.datetime.now()
    
    p = canvas.Canvas(response, bottomup=0, pagesize=letter)

    vertValue = 40
    p.drawString(30, vertValue, "Vehicle")
    p.drawString(85, vertValue, "Priority")
    p.drawString(130, vertValue, "Reason")
    p.drawString(220, vertValue, "Problem")
    #add date that the report was generated
    p.drawString(420, vertValue, now.strftime("Report Generated %m/%d/%Y"))
    vertValue=70

    page_entry=1
    page_number=1
    for issue in issue_list:
        if (page_entry==36):
            p.drawString(550, vertValue, "page {0}".format(page_number))
            page_entry=1
            page_number+=1
            p.showPage()
            vertValue=40
            p.drawString(30, vertValue, "Vehicle")
            p.drawString(85, vertValue, "Priority")
            p.drawString(130, vertValue, "Reason")
            p.drawString(220, vertValue, "Problem")
            #add date that the report was generated
            p.drawString(420, vertValue, now.strftime("Report Generated %m/%d/%Y"))
            vertValue=70

        p.drawString(30, vertValue, issue.vehicle.vehicle_name)
        p.drawString(85, vertValue, issue.severity)
        p.drawString(130, vertValue, issue.reason)
        p.drawString(220, vertValue, issue.description)
        vertValue = vertValue + 20
        page_entry+=1

    p.drawString(550, 770, "page {0}".format(page_number))
    p.showPage()
    p.save()
    return response
