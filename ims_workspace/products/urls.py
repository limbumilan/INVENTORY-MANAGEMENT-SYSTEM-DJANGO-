from django.urls import path
from . import views

urlpatterns = [
    # This leaves the route blank so it acts as the homepage for this app section
    path('', views.inventory_dashboard, name='inventory_dashboard'),
    path('export/csv/', views.export_inventory_csv, name='export_inventory_csv'),
]