from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('a-propos/', views.apropos_view, name='a_propos'),
    path('contact/', views.contact_view, name='contact'),
    # Endpoint de santé — pingé toutes les 5 min par UptimeRobot pour 24/7
    path('health/', views.health_check, name='health_check'),
    # SEO Moteurs de recherche (Google, Bing, DuckDuckGo...)
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
]
