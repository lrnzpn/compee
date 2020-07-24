from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)

# Create your views here.
def MainDashboard(request):
    return render(request, 'admins/dashboard.html')

