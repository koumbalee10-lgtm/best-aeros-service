from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from catalogue.models import Drone, Forfait, LieuFormation
from formations.models import SessionFormation
import datetime

User = get_user_model()

class Command(BaseCommand):
    help = 'Initialise les données officielles du Gabon pour BEST AÉROS SERVICE'

    def handle(self, *args, **options):
        self.stdout.write("Initialisation des données gabonaises...")

        # 1. Admin Michel Lee (préservé absolument)
        admin_user, created = User.objects.get_or_create(
            email='koumbalee10@gmail.com',
            defaults={
                'username': 'koumbalee10@gmail.com',
                'first_name': 'Lee Michel',
                'last_name': 'Koumba',
                'role': 'admin',
                'telephone': '+241 07 78 45 12',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('adminadmin')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("✓ Admin Michel créé (koumbalee10@gmail.com / adminadmin)"))

        # 2. DG Jean-Pierre Moussavou
        dg_user, created = User.objects.get_or_create(
            email='dg.moussavou@bestaeros.ga',
            defaults={
                'username': 'dg.moussavou@bestaeros.ga',
                'first_name': 'Jean-Pierre',
                'last_name': 'Moussavou',
                'role': 'dg',
                'telephone': '+241 06 22 34 56',
                'is_staff': True,
            }
        )
        if created:
            dg_user.set_password('dg2026')
            dg_user.save()
            self.stdout.write(self.style.SUCCESS("✓ DG Jean-Pierre Moussavou créé (dg.moussavou@bestaeros.ga / dg2026)"))

        # 3. Client Gabon
        client_user, created = User.objects.get_or_create(
            email='patrick.obame@gmail.com',
            defaults={
                'username': 'patrick.obame@gmail.com',
                'first_name': 'Patrick',
                'last_name': 'Obame Ndong',
                'role': 'client',
                'telephone': '+241 07 45 89 12',
            }
        )
        if created:
            client_user.set_password('client2026')
            client_user.save()
            self.stdout.write(self.style.SUCCESS("✓ Client Patrick Obame créé"))

        # 4. Lieux au Gabon
        lieux = [
            ("Piste Aéromodélisme d'Angondjé", "Libreville", "Carrefour Amissa, Angondjé", 12),
            ("Centre de Vol Tactique d'Essassi", "Libreville", "PK 24 Route Nationale 1", 15),
            ("Zone Spéciale Économique de Nkok", "Nkok", "Parc Technologique ZERP", 10),
            ("Piste Littorale de Port-Gentil", "Port-Gentil", "Cap Lopez, Zone Pétrolière", 8),
            ("Site d'Évolution des Plateaux Batéké", "Franceville", "Aérodrome de Mvengué", 10),
        ]
        for nom, ville, adr, cap in lieux:
            LieuFormation.objects.get_or_create(
                nom=nom,
                defaults={'ville': ville, 'adresse': adr, 'capacite_max': cap}
            )

        # 5. Forfaits
        forfaits = [
            ("Initiation & Découverte ANAC", "Bases du télépilotage, réglementation gabonaise et premiers vols à vue.", 2, 180000, "Débutant"),
            ("Télépilote Professionnel Civil", "Préparation complète au brevet d'aptitude théorique et pratique ANAC.", 5, 290000, "Le plus populaire"),
            ("Cartographie & Photogrammétrie RTK", "Modélisation 3D, relevés par drone et intégration SIG pour géomètres.", 5, 380000, "Expertise BTP"),
            ("Inspection Thermique & Industrielle", "Thermographie infrarouge appliquée aux torchères, pipelines et cuves.", 4, 450000, "Pétrole & Mines"),
            ("Pulvérisation Agricole & Forêt", "Épandage précis et télédétection pour plantations d'hévéa et palmiers.", 5, 490000, "Agriculture 4.0"),
        ]
        for nom, desc, duree, prix, badge in forfaits:
            Forfait.objects.get_or_create(
                nom=nom,
                defaults={'description': desc, 'duree_jours': duree, 'prix_fcfa': prix, 'badge': badge}
            )

        # 6. Drones
        drones = [
            ("DJI Mini 4 Pro Fly More Combo", "DJI", "Léger & Prise de vue", "Drone ultra-léger < 249g certifié ANAC, capteur 4K HDR vertical, idéal inspection rapide et vidéo.", 34, 20.0, "4K/60fps HDR", 249, 58, 11, 750000, 5, "img/drones/dji-mini-4-pro.svg", "Compact"),
            ("DJI Air 3 Pro Pack", "DJI", "Semi-Professionnel", "Double caméra principale moyen-télé 3x et grand-angle, transmission O4 20 km, résistance équatoriale.", 46, 20.0, "Double 4K 1/1.3\" CMOS", 720, 75, 12, 1100000, 4, "img/drones/dji-air-3.svg", "Polyvalent"),
            ("DJI Mavic 3 Enterprise RTK", "DJI", "Cartographie & Topographie", "Obturateur mécanique 0.7s, module RTK centimétrique, zoom hybride 56x pour géomètres gabonais.", 45, 15.0, "4/3 CMOS 20 MP Mécanique", 915, 75, 12, 2850000, 3, "img/drones/dji-mavic-3-enterprise.svg", "Précision RTK"),
            ("Autel EVO II Dual 640T V3", "Autel", "Thermique & Pétrole", "Caméra thermique radiométrique 640x512 + 8K visible. Idéal pour sites pétroliers de Port-Gentil.", 38, 15.0, "Thermique 640x512 + 8K", 1150, 72, 12, 3400000, 2, "img/drones/autel-evo-2-dual.svg", "Thermique"),
            ("DJI Matrice 350 RTK Industrie", "DJI", "Industriel Lourd IP55", "Plateforme industrielle tropicalisée IP55, 6 directions d'évitement d'obstacles, charge utile 2.7 kg.", 55, 20.0, "Multi-capteurs Zenmuse H20N", 3770, 83, 15, 6200000, 2, "img/drones/dji-matrice-350-rtk.svg", "Industriel Lourd"),
            ("DJI Agras T25 Agricole", "DJI", "Agriculture & Forêt", "Drone d'épandage agricole 20 kg et pulvérisation 20L, débit 16 L/min, radar actif phased array.", 20, 5.0, "Caméra FPV HD orientable", 25400, 36, 6, 8500000, 1, "img/drones/dji-agras-t25.svg", "Épandage 20L"),
        ]
        for nom, marque, cat, desc, auto, port, cam, poids, vit, vent, prix, stock, legacy, badge in drones:
            Drone.objects.get_or_create(
                nom=nom,
                defaults={
                    'marque': marque,
                    'categorie': cat,
                    'description': desc,
                    'autonomie_minutes': auto,
                    'portee_km': port,
                    'resolution_camera': cam,
                    'poids_grammes': poids,
                    'vitesse_max_kmh': vit,
                    'resistance_vent_ms': vent,
                    'prix_fcfa': prix,
                    'stock': stock,
                    'image_url_legacy': legacy,
                    'badge': badge,
                    'homologation_anac': True,
                }
            )

        self.stdout.write(self.style.SUCCESS("✓ Toutes les données du Gabon ont été insérées avec succès !"))
