from django.contrib import admin
from .models import SessionFormation, Reservation, Facture, FactureLigne, Notification, Commentaire

@admin.register(SessionFormation)
class SessionFormationAdmin(admin.ModelAdmin):
    list_display = ('forfait', 'lieu', 'date_debut', 'date_fin', 'places_total', 'statut')
    list_filter = ('statut', 'lieu__ville')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'forfait', 'session', 'statut', 'paye', 'date_reservation')
    list_filter = ('statut', 'paye')
    search_fields = ('client__email', 'client__first_name', 'client__last_name')

class FactureLigneInline(admin.TabularInline):
    model = FactureLigne
    extra = 1

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('numero', 'client', 'statut', 'montant_ttc', 'date_emission')
    list_filter = ('statut', 'date_emission')
    search_fields = ('numero', 'client__email', 'client__last_name')
    inlines = [FactureLigneInline]

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'message', 'lu', 'date_creation')

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('client', 'message', 'date_creation')
