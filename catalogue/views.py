from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Drone, Forfait

def drones_list(request):
    categorie = request.GET.get('categorie', '')
    drones = Drone.objects.filter(actif=True)
    if categorie:
        drones = drones.filter(categorie__icontains=categorie)
    return render(request, 'catalogue/drones.html', {
        'drones': drones,
        'categorie_active': categorie,
    })

def forfaits_list(request):
    forfaits = Forfait.objects.filter(actif=True)
    return render(request, 'catalogue/forfaits.html', {
        'forfaits': forfaits,
    })

@login_required
def changer_photo_drone_ajax(request):
    user = request.user
    if not (user.role in ['admin', 'dg'] or user.is_superuser):
        return JsonResponse({'succes': False, 'message': 'Non autorisé.'}, status=403)

    if request.method == 'POST':
        id_drone = request.POST.get('id_drone')
        drone = get_object_or_404(Drone, id=id_drone)

        if request.FILES.get('photo_drone'):
            drone.image = request.FILES['photo_drone']
            drone.save()
            return JsonResponse({
                'succes': True,
                'message': f"Photo du drone « {drone.nom} » mise à jour avec succès !",
                'image_url': drone.image.url
            })
        elif request.POST.get('image_url_directe'):
            drone.image_url_legacy = request.POST.get('image_url_directe')
            drone.save()
            return JsonResponse({
                'succes': True,
                'message': f"Lien du drone « {drone.nom} » mis à jour !",
                'image_url': drone.get_image_url()
            })

    return JsonResponse({'succes': False, 'message': 'Requête invalide.'})
