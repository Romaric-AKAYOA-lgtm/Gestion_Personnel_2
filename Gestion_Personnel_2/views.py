from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import timedelta, date
from EmployeMission.models import CLEmployeMission
from connection.views import get_connected_user
from Employe.models import CLEmploye
from Stagiaire.models import CLStagiaire
from mission.models import CLMission
from fonction.models import Fonction
from mutation.models import CLMutation
from Conge.models import CLConge  # <-- Ajout import du modèle Congé


def home_view(request):
    username = get_connected_user(request)

    if not username:
        return redirect('connection:login')

    today = timezone.now().date()

    # 1. Employés actifs
    employes_actifs = CLEmploye.objects.filter(tstt_user='actif')

    # 2. Employés qui partent en retraite cette année
    employes_retraite_cette_annee = CLEmploye.objects.filter(
        date_retraite__year=today.year
    )

    # 3. Employés avec moins de 6 mois de fonction
    six_months_ago = today - timedelta(days=6 * 30)
    employes_moins_6_mois = CLEmploye.objects.filter(dsb__gt=six_months_ago)

    # 4. Stagiaires de cette année
    stagiaires_de_cette_annee = CLStagiaire.objects.filter(
        dsb__year=today.year
    )

    # 5. Missions prévues dans 2 mois et non terminées
    dans_2_mois = today + timedelta(days=60)
    missions_dans_2_mois = CLMission.objects.filter(
        date_debut__month=dans_2_mois.month,
        date_debut__year=dans_2_mois.year,
        conclusion_mission__isnull=True
    )

    missions_employes_statut = []
    for mission in missions_dans_2_mois:
        employes_mission = CLEmployeMission.objects.filter(mission=mission).select_related('employe')
        employes_info = [
            {'nom': em.employe.nom, 'prenom': em.employe.prenom, 'statut': em.statut}
            for em in employes_mission
        ]
        missions_employes_statut.append({
            'mission': mission,
            'employes': employes_info,
        })

    # 6. Mutations hiérarchisées par unité (année en cours)
    annee_actuelle = date.today().year
    mutations_hierarchiques = CLMutation.objects.filter(
        date_debut__year=annee_actuelle
    ).select_related(
        'employe', 'function', 'organizational_unit'
    ).order_by(
        'organizational_unit__name',
        'function__designation'
    )

    # 7. Tranches d’âge
    employes_moins_20 = CLEmploye.objects.filter(
        dns__gte=today - timedelta(days=20 * 365)
    )
    employes_entre_30_50 = CLEmploye.objects.filter(
        dns__lte=today - timedelta(days=30 * 365),
        dns__gte=today - timedelta(days=50 * 365)
    )
    employes_entre_50_60 = CLEmploye.objects.filter(
        dns__lte=today - timedelta(days=50 * 365),
        dns__gte=today - timedelta(days=60 * 365)
    )
    employes_plus_60 = CLEmploye.objects.filter(
        dns__lte=today - timedelta(days=60 * 365)
    )

    # 8. Congés
    en_conge = CLConge.objects.filter(
        date_debut_previsionnel__lte=today,
        date_retour_previsionnel__gte=today,
        date_retour_definitif__isnull=True
    )

    partent_aujourdhui = CLConge.objects.filter(
        date_debut_previsionnel=today
    )

    reviennent_aujourdhui = CLConge.objects.filter(
        date_retour_previsionnel=today
    )

    context = {
        'username': username,
        'employes_actifs': employes_actifs,
        'employes_retraite_cette_annee': employes_retraite_cette_annee,
        'employes_moins_6_mois': employes_moins_6_mois,
        'nombre_moins_20': employes_moins_20.count(),
        'nombre_entre_30_50': employes_entre_30_50.count(),
        'nombre_entre_50_60': employes_entre_50_60.count(),
        'nombre_plus_60': employes_plus_60.count(),
        'nombre_stagiaires': stagiaires_de_cette_annee.count(),
        'stagiaires_de_cette_annee': stagiaires_de_cette_annee,
        'missions_employes_statut': missions_employes_statut,
        'mutations_hierarchiques': mutations_hierarchiques,
        'en_conge': en_conge,
        'partent_aujourdhui': partent_aujourdhui,
        'reviennent_aujourdhui': reviennent_aujourdhui,
    }

    return render(request, "home.html", context)
