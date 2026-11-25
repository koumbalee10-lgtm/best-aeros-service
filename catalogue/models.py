from django.db import models

class Forfait(models.Model):
    nom = models.CharField('Nom du forfait', max_length=150)
    description = models.TextField('Description détaillée')
    duree_jours = models.PositiveIntegerField('Durée en jours', default=5)
    prix_fcfa = models.PositiveIntegerField('Prix en FCFA (XAF)')
    badge = models.CharField('Badge accroche', max_length=50, blank=True)
    actif = models.BooleanField('Actif sur le site', default=True)

    class Meta:
        verbose_name = 'Forfait de formation'
        verbose_name_plural = 'Forfaits de formation'
        ordering = ['prix_fcfa']

    def __str__(self):
        return f"{self.nom} - {self.prix_fcfa:,} FCFA".replace(',', ' ')


class Drone(models.Model):
    nom = models.CharField('Modèle du drone', max_length=150)
    marque = models.CharField('Marque constructeur', max_length=80, default='DJI')
    categorie = models.CharField('Catégorie d\'usage', max_length=100)
    description = models.TextField('Description technique')
    autonomie_minutes = models.PositiveIntegerField('Autonomie (minutes)', default=30)
    portee_km = models.DecimalField('Portée max (km)', max_digits=4, decimal_places=1, default=10.0)
    resolution_camera = models.CharField('Capteur vidéo / caméra', max_length=120)
    poids_grammes = models.PositiveIntegerField('Poids en vol (g)', default=500)
    vitesse_max_kmh = models.PositiveIntegerField('Vitesse max (km/h)', default=75)
    resistance_vent_ms = models.PositiveIntegerField('Résistance vent (m/s)', default=12)
    homologation_anac = models.BooleanField('Homologué ANAC Gabon', default=True)
    prix_fcfa = models.PositiveIntegerField('Prix unitaire FCFA (XAF)')
    stock = models.PositiveIntegerField('Stock disponible à Libreville', default=3)
    image = models.ImageField('Photo du drone', upload_to='drones/', blank=True, null=True)
    image_url_legacy = models.CharField('Chemin SVG fallback', max_length=255, blank=True)
    badge = models.CharField('Badge produit', max_length=50, blank=True)
    actif = models.BooleanField('Visible catalogue', default=True)

    class Meta:
        verbose_name = 'Drone'
        verbose_name_plural = 'Drones Homologués'
        ordering = ['prix_fcfa']

    def __str__(self):
        return f"{self.nom} ({self.categorie})"

    def get_image_url(self):
        if self.image:
            return self.image.url
        if self.image_url_legacy:
            return f"/static/{self.image_url_legacy}"
        return "/static/img/drones/dji-mini-4-pro.svg"


class LieuFormation(models.Model):
    nom = models.CharField('Nom du site / terrain', max_length=150)
    ville = models.CharField('Ville au Gabon', max_length=100, default='Libreville')
    adresse = models.CharField('Adresse / Emplacement', max_length=255)
    capacite_max = models.PositiveIntegerField('Capacité maximale', default=12)
    actif = models.BooleanField('Actif', default=True)

    class Meta:
        verbose_name = 'Lieu de formation'
        verbose_name_plural = 'Lieux de formation Gabon'
        ordering = ['ville', 'nom']

    def __str__(self):
        return f"{self.nom} ({self.ville})"
