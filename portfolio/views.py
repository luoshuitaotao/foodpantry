
from django.utils import timezone
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import Sum
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import serializers
from portfolio.serializers import PortfolioSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response


def index(request):
    html = TemplateResponse(request, 'inventory_list.html')
    return HttpResponse(html.render())

def password_reset(request):
    return render(request, 'registration/password_reset_form.html',
    {'portfolio': password_reset})


def password_reset_confirm(request):
    return render(request, 'registration/password_reset_confirm.html',
    {'portfolio': password_reset_confirm})

def password_reset_email(request):
    return render(request, 'registration/password_reset_email.html',
    {'portfolio': password_reset_email})

def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html',
    {'portfolio': password_reset_complete})


def abc(request):
    return render(request, 'portfolio/abc.html')

@login_required
def home(request):
   return render(request, 'portfolio/home.html',
                 {'home':home})

@staff_member_required
def home2(request):
   return render(request, 'portfolio/home2.html',
                 {'home2':home2})


@staff_member_required
def volunteer_list(request):
   volunteer = Volunteer.objects.filter(created_date__lte=timezone.now())
   return render(request, 'portfolio/volunteer_list.html',
                 {'volunteers': volunteer})

@login_required
def volunteer_new(request):
   if request.method == "POST":
       form = VolunteerForm(request.POST)
       if form.is_valid():
           volunteer = form.save(commit=False)
           volunteer.created_date = timezone.now()
           volunteer.save()
           volunteers = Volunteer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'portfolio/volunteer_list.html',
                         {'volunteers': volunteers})
   else:
       form = VolunteerForm()
       # print("Else")
   return render(request, 'portfolio/volunteer_new.html', {'form': form})

@login_required
def volunteer_edit(request, pk):
   volunteer = get_object_or_404(Volunteer, pk=pk)
   if request.method == "POST":
       # update
       form = VolunteerForm(request.POST, instance=volunteer)
       if form.is_valid():
           volunteer = form.save(commit=False)
           volunteer.updated_date = timezone.now()
           volunteer.save()
           volunteer = Volunteer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'portfolio/volunteer_list.html',
                         {'volunteers': volunteer})
   else:
       # edit
       form = VolunteerForm(instance=volunteer)
   return render(request, 'portfolio/volunteer_edit.html', {'form': form})


@login_required
def volunteer_delete(request, pk):
   volunteer = get_object_or_404(Volunteer, pk=pk)
   volunteer.delete()
   return redirect('portfolio:volunteer_list')



@login_required
class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    def inventory_list(request):
       inventorys = Inventory.objects.filter(acquired_date__lte=timezone.now())
       return render(request, 'portfolio/inventory_list.html', {'inventorys': inventorys})

@staff_member_required
def inventory_list2(request):
   inventorys = Inventory.objects.filter(acquired_date__lte=timezone.now())
   return render(request, 'portfolio/inventory_list2.html', {'inventorys': inventorys})


@login_required
def inventory_new(request):
   if request.method == "POST":
       form = InventoryForm(request.POST)
       if form.is_valid():
           inventory = form.save(commit=False)
           inventory.created_date = timezone.now()
           inventory.save()
           inventorys = Inventory.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/inventory_list.html',
                         {'inventorys': inventorys})
   else:
       form = InventoryForm()
       # print("Else")
   return render(request, 'portfolio/inventory_new.html', {'form': form})


@login_required
def inventory_edit(request, pk):
   inventory = get_object_or_404(Inventory, pk=pk)
   if request.method == "POST":
       form = InventoryForm(request.POST, instance=inventory)
       if form.is_valid():
           inventory = form.save()
           inventory.updated_date = timezone.now()
           inventory.save()
           inventorys = Inventory.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/inventory_list.html', {'inventorys': inventorys})
   else:
       # print("else")
       form = InventoryForm(instance=inventory)
   return render(request, 'portfolio/inventory_edit.html', {'form': form})


@login_required
def inventory_delete(request, pk):
   inventory = get_object_or_404(Inventory, pk=pk)
   inventory.delete()
   inventorys = Inventory.objects.filter(acquired_date__lte=timezone.now())
   return render(request, 'portfolio/inventory_list.html', {'inventorys': inventorys})
