from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('connexion/', views.user_login, name='login'),
    path('deconnexion/', views.user_logout, name='logout'),
    path('inscription/', views.user_register, name='register'),
    path('profil/', views.profile_view, name='profile'),
    path('api/changer-avatar/', views.changer_avatar_ajax, name='changer_avatar'),

    # Réinitialisation de mot de passe
    path('mot-de-passe-oublie/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.txt',
             subject_template_name='accounts/password_reset_subject.txt',
         ),
         name='password_reset'),
    path('mot-de-passe-oublie/envoye/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reinitialiser/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url='/accounts/reinitialiser/succes/'
         ),
         name='password_reset_confirm'),
    path('reinitialiser/succes/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    # Changement de mot de passe (connecté)
    path('changer-mot-de-passe/',
         auth_views.PasswordChangeView.as_view(
             template_name='accounts/password_change.html',
             success_url='/accounts/changer-mot-de-passe/succes/'
         ),
         name='password_change'),
    path('changer-mot-de-passe/succes/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='accounts/password_change_done.html'
         ),
         name='password_change_done'),
]
