from django.shortcuts import render,redirect
from django.views.generic import TemplateView



class JobseekerDashboardView(TemplateView):
    template_name = 'Dashboard/Dashboard.html'
class AdminDashboardView(TemplateView):
    template_name = 'Dashboard/AdminDashboard.html'




class HomeDashboardView(TemplateView):
    template_name = 'dash/shome.html'


