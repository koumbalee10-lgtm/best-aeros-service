# 🚀 Guide de Déploiement — BEST AÉROS SERVICE Django
## Render.com + UptimeRobot → Site en ligne 24h/24 7j/7 GRATUITEMENT

---

## ÉTAPE 1 — Pousser le code sur GitHub

```bash
cd best_aeros_django/

# Initialiser Git (si pas encore fait)
git init
git add .
git commit -m "🚀 BEST AÉROS SERVICE Django — Prêt pour Render.com"
git branch -M main

# Créer un dépôt GitHub (sur github.com) puis :
git remote add origin https://github.com/VOTRE_USERNAME/best-aeros-service.git
git push -u origin main
```

---

## ÉTAPE 2 — Déployer sur Render.com (gratuit)

1. Aller sur **https://render.com** → Créer un compte gratuit (avec GitHub)
2. Tableau de bord → **New** → **Blueprint**
3. Sélectionner votre dépôt `best-aeros-service`
4. Render lit le `render.yaml` et crée automatiquement :
   - ✅ Service web Python (Gunicorn)
   - ✅ Base de données PostgreSQL (Frankfurt)
5. Cliquer **Apply** → Attendre ~3 minutes

### Votre site sera accessible à :
```
https://best-aeros-service.onrender.com
```

### Accès Admin Django :
```
https://best-aeros-service.onrender.com/admin/
Email    : koumbalee10@gmail.com
Password : adminadmin   ← À CHANGER IMMÉDIATEMENT EN PRODUCTION
```

---

## ÉTAPE 3 — Configurer UptimeRobot pour le 24/7 🔁

> Sans cette étape, le site "dort" après 15 min sans visiteur (plan gratuit Render).
> UptimeRobot le "réveille" en le pingant toutes les 5 minutes → **disponibilité 24h/24**.

### 3.1 Créer un compte UptimeRobot (100% gratuit)
1. Aller sur **https://uptimerobot.com** → **Register for FREE**
2. Confirmer votre email

### 3.2 Ajouter un moniteur
1. Dashboard UptimeRobot → **+ Add New Monitor**
2. Remplir le formulaire :
   - **Monitor Type** : `HTTP(s)`
   - **Friendly Name** : `BEST AÉROS SERVICE - Gabon`
   - **URL** : `https://best-aeros-service.onrender.com/health/`
   - **Monitoring Interval** : `5 minutes` ✅
3. Cliquer **Create Monitor**

### 3.3 Résultat
- UptimeRobot pingera `/health/` toutes les **5 minutes**
- Render ne mettra **jamais** le serveur en veille
- Vous recevrez un **email d'alerte** si le site tombe
- Tableau de bord de disponibilité avec statistiques (uptime %)

### Endpoint de santé utilisé :
```
GET https://best-aeros-service.onrender.com/health/

Réponse :
{
  "status": "ok",
  "service": "BEST AÉROS SERVICE",
  "location": "Libreville, Gabon",
  "timestamp": "2026-11-25T21:00:00+00:00",
  "uptime": "24/7"
}
```

---

## ÉTAPE 4 — Vérifier le déploiement

```bash
# Tester le site
curl https://best-aeros-service.onrender.com/health/

# Tester la page d'accueil
curl -I https://best-aeros-service.onrender.com/
```

---

## Résumé des services gratuits utilisés

| Service | Rôle | Coût |
|:---|:---|:---:|
| **GitHub** | Hébergement code source + CI/CD | 0 € |
| **Render.com** | Hébergement Django + PostgreSQL | 0 € |
| **UptimeRobot** | Ping /health/ toutes les 5 min → 24/7 | 0 € |
| **Let's Encrypt** | Certificat HTTPS automatique | 0 € |
| **WhiteNoise** | Serveur fichiers statiques | 0 € |
| **TOTAL** | | **0 €/mois** |

---

## En cas de problème

```bash
# Voir les logs en temps réel sur Render :
# Dashboard → best-aeros-service → Logs

# Redéployer manuellement :
git add . && git commit -m "fix" && git push
# → Render redéploie automatiquement en 2-3 minutes
```

---

## Passer en production commerciale (optionnel)

Quand le site génère du trafic réel, passer au plan **Render Starter ($7/mois)** pour :
- ✅ Domaine personnalisé `bestaeros.ga`
- ✅ Zéro cold start (instance toujours active)
- ✅ PostgreSQL 1 Go (sans suppression automatique)
- ✅ 400 heures de build/mois
