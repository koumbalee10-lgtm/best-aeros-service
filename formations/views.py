from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import SessionFormation, Reservation, Facture, FactureLigne, Notification, Commentaire
from catalogue.models import Forfait, Drone, LieuFormation
import datetime

def sessions_list(request):
    ville = request.GET.get('ville', '')
    sessions = SessionFormation.objects.filter(statut='publiee', date_debut__gte=timezone.now().date())
    if ville:
        sessions = sessions.filter(lieu__ville__iexact=ville)
    villes = LieuFormation.objects.values_list('ville', flat=True).distinct()
    return render(request, 'formations/sessions.html', {
        'sessions': sessions,
        'villes': villes,
        'ville_active': ville,
    })

@login_required
def client_dashboard(request):
    reservations = Reservation.objects.filter(client=request.user).select_related('forfait', 'session', 'session__lieu', 'drone')
    notifications = Notification.objects.filter(utilisateur=request.user)[:5]
    Notification.objects.filter(utilisateur=request.user, lu=False).update(lu=True)
    return render(request, 'formations/client_dashboard.html', {
        'reservations': reservations,
        'notifications': notifications,
    })

@login_required
def reserver_view(request):
    forfait_id = request.GET.get('forfait') or request.POST.get('forfait')
    drone_id = request.GET.get('drone') or request.POST.get('drone')

    if request.method == 'POST':
        forfait = get_object_or_404(Forfait, id=request.POST.get('forfait'))
        session_id = request.POST.get('session')
        session = SessionFormation.objects.filter(id=session_id).first() if session_id else None
        drone = Drone.objects.filter(id=drone_id).first() if drone_id else None
        remarques = request.POST.get('remarques', '').strip()

        res = Reservation.objects.create(
            client=request.user,
            forfait=forfait,
            session=session,
            drone=drone,
            remarques=remarques,
            statut='en_attente'
        )

        # Créer une notification pour l'utilisateur
        Notification.objects.create(
            utilisateur=request.user,
            message=f"Votre demande pour le forfait « {forfait.nom} » a bien été transmise à la Direction Générale."
        )

        messages.success(request, "Votre réservation a été soumise avec succès ! Le Directeur Général validera votre session sous 24h.")
        return redirect('formations:client_dashboard')

    forfaits = Forfait.objects.filter(actif=True)
    sessions = SessionFormation.objects.filter(statut='publiee', date_debut__gte=timezone.now().date())
    drones = Drone.objects.filter(actif=True)

    return render(request, 'formations/reserver.html', {
        'forfaits': forfaits,
        'sessions': sessions,
        'drones': drones,
        'forfait_preselection': forfait_id,
        'drone_preselection': drone_id,
    })

@login_required
def dg_dashboard(request):
    if not request.user.is_dg:
        messages.error(request, "Accès réservé à la Direction Générale.")
        return redirect('core:home')

    en_attente = Reservation.objects.filter(statut='en_attente').count()
    confirmees = Reservation.objects.filter(statut='confirmee').count()
    sessions_ouvertes = SessionFormation.objects.filter(statut='publiee').count()
    dernieres_res = Reservation.objects.select_related('client', 'forfait', 'session', 'session__lieu').order_by('-date_reservation')[:8]

    return render(request, 'formations/dg_dashboard.html', {
        'en_attente': en_attente,
        'confirmees': confirmees,
        'sessions_ouvertes': sessions_ouvertes,
        'dernieres_res': dernieres_res,
    })

@login_required
def dg_valider_reservation(request, reservation_id, action):
    if not request.user.is_dg:
        return redirect('core:home')

    res = get_object_or_404(Reservation, id=reservation_id)
    if action == 'valider':
        res.statut = 'confirmee'
        Notification.objects.create(
            utilisateur=res.client,
            message=f"Bonne nouvelle ! Votre réservation pour « {res.forfait.nom} » a été CONFIRMÉE par la Direction Générale."
        )
        messages.success(request, f"Réservation #{res.id} confirmée.")
    elif action == 'refuser':
        res.statut = 'refusee'
        Notification.objects.create(
            utilisateur=res.client,
            message=f"Votre réservation pour « {res.forfait.nom} » a été refusée (session complète ou contrainte technique)."
        )
        messages.info(request, f"Réservation #{res.id} refusée.")
    elif action == 'payer':
        res.paye = True
        messages.success(request, f"Paiement pour la réservation #{res.id} enregistré.")

    res.save()
    return redirect('formations:dg_dashboard')

@login_required
def dg_factures_list(request):
    if not request.user.is_dg:
        return redirect('core:home')

    factures = Facture.objects.select_related('client').order_by('-date_emission')
    return render(request, 'formations/dg_factures.html', {
        'factures': factures,
    })

@login_required
def facture_detail(request, facture_id):
    facture = get_object_or_404(Facture.objects.select_related('client', 'createur', 'reservation'), id=facture_id)
    # Vérification des droits : DG, Admin, ou le client propriétaire
    if not (request.user.is_dg or request.user == facture.client):
        messages.error(request, "Accès non autorisé à cette facture.")
        return redirect('core:home')

    return render(request, 'formations/facture_detail.html', {
        'facture': facture,
        'lignes': facture.lignes.all(),
    })


@login_required
def avis_view(request):
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        if message:
            Commentaire.objects.create(client=request.user, message=message)
            messages.success(request, "Merci ! Votre avis a bien été enregistré.")
            return redirect('formations:avis')
        else:
            messages.error(request, "Veuillez saisir votre avis avant de l'envoyer.")

    mes_avis = Commentaire.objects.filter(client=request.user)
    return render(request, 'formations/avis.html', {
        'mes_avis': mes_avis,
    })
