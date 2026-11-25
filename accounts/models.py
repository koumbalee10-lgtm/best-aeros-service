from django.db import models
from django.contrib.auth.models import AbstractUser
import urllib.parse

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur Principal'),
        ('dg', 'Directeur Général (DG)'),
        ('client', 'Client / Télépilote'),
    ]

    email = models.EmailField('Adresse email', unique=True)
    role = models.CharField('Rôle', max_length=15, choices=ROLE_CHOICES, default='client')
    telephone = models.CharField('Téléphone Gabon', max_length=25, blank=True)
    whatsapp = models.CharField('Numéro WhatsApp', max_length=25, blank=True)
    photo_profil = models.ImageField('Photo de profil', upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        nom_complet = f"{self.first_name} {self.last_name}".strip()
        return f"{nom_complet} ({self.get_role_display()})" if nom_complet else self.email

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_dg(self):
        return self.role == 'dg' or self.role == 'admin' or self.is_superuser

    @property
    def initials(self):
        p = self.first_name[0].upper() if self.first_name else 'B'
        n = self.last_name[0].upper() if self.last_name else 'A'
        return f"{p}{n}"

    def get_avatar_url(self):
        if self.photo_profil:
            return self.photo_profil.url
        # Avatar SVG initiales dégradé aero
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">'
            f'<defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">'
            f'<stop offset="0%" stop-color="#0F172A"/><stop offset="100%" stop-color="#1E3A8A"/>'
            f'</linearGradient></defs>'
            f'<circle cx="50" cy="50" r="50" fill="url(#g)"/>'
            f'<text x="50%" y="54%" font-family="Inter, system-ui, sans-serif" font-size="40" font-weight="700" fill="#F8FAFC" text-anchor="middle" dominant-baseline="middle">{self.initials}</text>'
            f'</svg>'
        )
        return 'data:image/svg+xml;utf8,' + urllib.parse.quote(svg)
