from django.contrib import admin
from .models import Forfait, Drone, LieuFormation

@admin.register(Forfait)
class ForfaitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'duree_jours', 'prix_fcfa', 'actif')
    list_filter = ('actif',)

@admin.register(Drone)
class DroneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'marque', 'categorie', 'prix_fcfa', 'stock', 'homologation_anac', 'actif')
    list_filter = ('categorie', 'homologation_anac', 'actif')
    search_fields = ('nom', 'description')

@admin.register(LieuFormation)
class LieuFormationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'capacite_max', 'actif')
    list_filter = ('ville', 'actif')
