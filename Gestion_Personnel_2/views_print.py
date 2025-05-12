# utils_pdf.py

import os
from django.shortcuts import redirect
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from django.utils.timezone import localtime

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from connection.views import get_connected_user

def generer_entete_pdf(p):
    """
    Ajoute l'entête du document PDF avec un logo centré et des lignes de texte officielles.
    """
    width, height = A4
    y = height - 50  # Position initiale en haut de la page
    line_height = 15

    # 📌 Chemin du logo à adapter selon l'arborescence de ton projet
    logo_path = os.path.join("chemin_vers_ton_dossier", "45906d1a-f183-41db-bfad-d4e6c14242fb.png")

    try:
        logo = ImageReader(logo_path)
        logo_width, logo_height = 120, 50
        p.drawImage(logo, (width - logo_width) / 2, y, width=logo_width, height=logo_height, mask='auto')
        y -= (logo_height + 10)
    except Exception as e:
        print(f"Erreur lors de l'affichage du logo : {e}")
        p.setFont("Times-Roman", 10)
        p.drawCentredString(width / 2, y, "Logo non disponible")
        y -= 20

    # Texte institutionnel
    lignes_entete = [
        "REPUBLIQUE DU CONGO",
        "Unité * Travail * Progrès",
        "",
        "------------------------------",
        "MINISTERE DE L’ENSEIGNEMENT PRESCOLAIRE, PRIMAIRE,",
        "SECONDAIRE ET DE L’ALPHABETISATION",
        "------------------------------",
        "C A B I N E T",
        "------------------------------",
        "INSTITUT NATIONAL DE RECHERCHE ET D’ACTION PEDAGOGIQUES",
        "",
        " : 2128 / Adresse : Avenue des 1ers Jeux Africains, Face Grande Bibliothèque Universitaire",
        "Email : inrapcongo242@gmail.com – Brazzaville"
    ]

    p.setFont("Times-Roman", 12)
    for ligne in lignes_entete:
        p.drawCentredString(width / 2, y, ligne)
        y -= line_height


def generer_pdf_avec_pied_de_page(p, user):
    """
    Ajoute le contenu principal et les informations de signature dans le PDF.
    """
    width, height = A4

    # Informations utilisateur en bas à droite
    x_offset_right = width - 200
    y_infos = 200

    date_du_jour = localtime().strftime("%d/%m/%Y")
    tnm = getattr(user, 'tnm', 'Nom inconnu').upper()
    tpm = getattr(user, 'tpm', 'Prénom inconnu')

    p.setFont("Times-Roman", 10)
    p.drawString(x_offset_right, y_infos, f"Fait à Brazzaville, le {date_du_jour}")
    p.drawString(x_offset_right, y_infos - 70, f"{tnm} {tpm}")

    return True


def generer_pdf_complet(request):
    username = get_connected_user(request)

    if not username:
        return redirect('connection:login')
    """
    Génère un PDF complet comprenant une entête et un contenu utilisateur.
    La réponse HTTP retourne le PDF généré.
    """
    # Récupérer l'utilisateur connecté (exemple basé sur la structure Django)
    user = request.user

    # Créer la réponse HTTP pour un fichier PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="document_complet.pdf"'

    # Créer le canvas PDF
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Ajouter l'entête du PDF
    generer_entete_pdf (p)  # Appelle la fonction pour ajouter l'entête

    # Ajouter le contenu spécifique à l'utilisateur
    generer_pdf_avec_pied_de_page(p, user)  # Appelle la fonction pour ajouter le contenu utilisateur

    # Finaliser le PDF et l'envoyer en réponse
    p.showPage()
    p.save()

    return response
