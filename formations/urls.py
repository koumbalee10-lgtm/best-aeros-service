from django.urls import path
from . import views

app_name = 'formations'

urlpatterns = [
    path('sessions/', views.sessions_list, name='sessions'),
    path('espace-client/', views.client_dashboard, name='client_dashboard'),
    path('reserver/', views.reserver_view, name='reserver'),
    path('espace-dg/', views.dg_dashboard, name='dg_dashboard'),
    path('espace-dg/action/<int:reservation_id>/<str:action>/', views.dg_valider_reservation, name='dg_action'),
    path('espace-dg/factures/', views.dg_factures_list, name='dg_factures'),
    path('factures/<int:facture_id>/', views.facture_detail, name='facture_detail'),
    path('avis/', views.avis_view, name='avis'),
]
