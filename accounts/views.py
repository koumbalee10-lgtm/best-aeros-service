from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import User

def user_login(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        mdp = request.POST.get('password', '')
        user = authenticate(request, username=email, password=mdp)
        if user:
            login(request, user)
            messages.success(request, f"Ravi de vous revoir, {user.first_name} !")
            if user.role == 'admin':
                return redirect('/admin/')
            elif user.role == 'dg':
                return redirect('formations:dg_dashboard')
            return redirect('formations:client_dashboard')
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('core:home')

def user_register(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        nom = request.POST.get('nom', '').strip()
        prenom = request.POST.get('prenom', '').strip()
        tel = request.POST.get('telephone', '').strip()
        whatsapp = request.POST.get('whatsapp', '').strip()
        mdp = request.POST.get('password', '')

        if not email or not nom or not prenom or not mdp:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Cette adresse email est déjà utilisée.")
        else:
            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=prenom,
                last_name=nom,
                telephone=tel,
                whatsapp=whatsapp,
                password=mdp,
                role='client'
            )
            login(request, user)
            messages.success(request, f"Bienvenue chez BEST AÉROS SERVICE, {prenom} !")
            return redirect('formations:client_dashboard')
    return render(request, 'accounts/register.html')

@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('prenom', user.first_name)
        user.last_name = request.POST.get('nom', user.last_name)
        user.telephone = request.POST.get('telephone', user.telephone)
        user.whatsapp = request.POST.get('whatsapp', user.whatsapp)
        if request.FILES.get('photo_profil'):
            user.photo_profil = request.FILES['photo_profil']
        user.save()
        messages.success(request, "Vos informations ont été mises à jour.")
        return redirect('accounts:profile')
    return render(request, 'accounts/profile.html')

@login_required
def changer_avatar_ajax(request):
    if request.method == 'POST' and request.FILES.get('photo_profil'):
        user = request.user
        user.photo_profil = request.FILES['photo_profil']
        user.save()
        return JsonResponse({
            'succes': True,
            'message': 'Photo de profil mise à jour avec succès !',
            'avatar_url': user.photo_profil.url
        })
    return JsonResponse({'succes': False, 'message': 'Aucun fichier reçu.'})
