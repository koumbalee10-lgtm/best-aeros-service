from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from catalogue.models import Forfait, Drone
from formations.models import SessionFormation
from django.utils import timezone
import datetime

def home_view(request):
    forfaits = Forfait.objects.filter(actif=True)[:3]
    drones_phares = Drone.objects.filter(actif=True)[:3]
    prochaines_sessions = SessionFormation.objects.filter(
        statut='publiee',
        date_debut__gte=timezone.now().date()
    ).select_related('forfait', 'lieu')[:3]

    return render(request, 'core/home.html', {
        'forfaits': forfaits,
        'drones_phares': drones_phares,
        'prochaines_sessions': prochaines_sessions,
    })

def apropos_view(request):
    return render(request, 'core/a_propos.html')

def contact_view(request):
    if request.method == 'POST':
        messages.success(request, "Merci ! Votre message a bien été envoyé. Notre équipe à Libreville vous contactera dans les plus brefs délais.")
    return render(request, 'core/contact.html')


def health_check(request):
    """
    Endpoint de santé pour maintenir le serveur éveillé 24h/24 7j/7.
    Pingé toutes les 5 minutes par UptimeRobot (service gratuit).
    Répond en < 50ms sans toucher à la base de données.
    """
    return JsonResponse({
        'status': 'ok',
        'service': 'BEST AÉROS SERVICE',
        'location': 'Libreville, Gabon',
        'timestamp': datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
        'uptime': '24/7',
    }, status=200)


def robots_txt(request):
    """Robots.txt dynamique à la racine pour Google, Bing, DuckDuckGo, etc."""
    base_url = request.build_absolute_uri('/').rstrip('/')
    lines = [
        "User-agent: *",
        "Allow: /",
        "Allow: /a-propos/",
        "Allow: /catalogue/drones/",
        "Allow: /catalogue/forfaits/",
        "Allow: /formations/sessions/",
        "Allow: /contact/",
        "Disallow: /admin/",
        "Disallow: /formations/espace-dg/",
        "Disallow: /formations/espace-client/",
        "Disallow: /accounts/",
        f"Sitemap: {base_url}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


def sitemap_xml(request):
    """Sitemap XML dynamique à la racine pour l'indexation sur tous les moteurs de recherche."""
    base_url = request.build_absolute_uri('/').rstrip('/')
    today = timezone.now().date().isoformat()
    pages = [
        ('/', 'daily', '1.0'),
        ('/a-propos/', 'weekly', '0.8'),
        ('/catalogue/drones/', 'daily', '0.9'),
        ('/catalogue/forfaits/', 'weekly', '0.9'),
        ('/formations/sessions/', 'daily', '0.8'),
        ('/contact/', 'monthly', '0.7'),
    ]
    urls_xml = "\n".join(
        f"  <url>\n    <loc>{base_url}{path}</loc>\n    <lastmod>{today}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>"
        for path, freq, prio in pages
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls_xml}\n"
        '</urlset>'
    )
    return HttpResponse(xml, content_type="application/xml; charset=utf-8")
