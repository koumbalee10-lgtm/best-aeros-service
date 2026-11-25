from django.db import models
from django.conf import settings
from catalogue.models import Forfait, Drone, LieuFormation
import datetime

class SessionFormation(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publiee', 'Publiée / Ouverte'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]

    forfait = models.ForeignKey(Forfait, on_delete=models.CASCADE, related_name='sessions')
    lieu = models.ForeignKey(LieuFormation, on_delete=models.CASCADE, related_name='sessions')
    date_debut = models.DateField('Date de début')
    date_fin = models.DateField('Date de fin')
    places_total = models.PositiveIntegerField('Nombre total de places', default=8)
    statut = models.CharField('Statut', max_length=15, choices=STATUT_CHOICES, default='publiee')

    class Meta:
        verbose_name = 'Session de formation'
        verbose_name_plural = 'Sessions de formation'
        ordering = ['date_debut']

    def __str__(self):
        return f"{self.forfait.nom} - {self.lieu.ville} (Du {self.date_debut.strftime('%d/%m')} au {self.date_fin.strftime('%d/%m/%Y')})"

    @property
    def places_restantes(self):
        confirmees = self.reservations.filter(statut='confirmee').count()
        return max(0, self.places_total - confirmees)


class Reservation(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('refusee', 'Refusée'),
        ('annulee', 'Annulée'),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    forfait = models.ForeignKey(Forfait, on_delete=models.CASCADE)
    session = models.ForeignKey(SessionFormation, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    drone = models.ForeignKey(Drone, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    date_reservation = models.DateTimeField('Date de réservation', auto_now_add=True)
    statut = models.CharField('Statut', max_length=15, choices=STATUT_CHOICES, default='en_attente')
    paye = models.BooleanField('Paiement réglé', default=False)
    remarques = models.TextField('Remarques client / besoin', blank=True)

    class Meta:
        verbose_name = 'Réservation'
        verbose_name_plural = 'Réservations clients'
        ordering = ['-date_reservation']

    def __str__(self):
        return f"Réservation #{self.id} - {self.client} ({self.forfait.nom})"

    @property
    def montant_total(self):
        total = self.forfait.prix_fcfa
        if self.drone:
            total += self.drone.prix_fcfa
        return total


class Facture(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('emise', 'Émise'),
        ('payee', 'Payée'),
        ('annulee', 'Annulée'),
    ]

    numero = models.CharField('Numéro de facture', max_length=30, unique=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='factures')
    reservation = models.OneToOneField(Reservation, on_delete=models.SET_NULL, null=True, blank=True, related_name='facture')
    createur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='factures_creees')
    statut = models.CharField('Statut', max_length=15, choices=STATUT_CHOICES, default='emise')
    date_emission = models.DateTimeField('Date d\'émission', auto_now_add=True)
    date_echeance = models.DateField('Date d\'échéance', null=True, blank=True)
    montant_ht = models.PositiveIntegerField('Montant HT (FCFA)', default=0)
    tva_pct = models.DecimalField('Taux TVA (%)', max_digits=5, decimal_places=2, default=18.00)
    montant_tva = models.PositiveIntegerField('Montant TVA (FCFA)', default=0)
    montant_ttc = models.PositiveIntegerField('Montant TTC (FCFA)', default=0)
    notes = models.TextField('Notes & conditions', blank=True)

    class Meta:
        verbose_name = 'Facture'
        verbose_name_plural = 'Factures (Historique long terme)'
        ordering = ['-date_emission']

    def __str__(self):
        return f"{self.numero} - {self.client} ({self.montant_ttc:,} FCFA)".replace(',', ' ')


class FactureLigne(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='lignes')
    description = models.CharField('Description', max_length=255)
    quantite = models.PositiveIntegerField('Quantité', default=1)
    prix_unitaire = models.PositiveIntegerField('Prix unitaire FCFA', default=0)
    total_ligne = models.PositiveIntegerField('Total ligne FCFA', default=0)

    def save(self, *args, **kwargs):
        self.total_ligne = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)


class Notification(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField('Message')
    lu = models.BooleanField('Lu', default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']


class Commentaire(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField('Avis / Suggestion')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']
