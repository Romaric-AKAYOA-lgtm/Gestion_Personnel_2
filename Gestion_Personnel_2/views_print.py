# utils_pdf.py

import os
from pydoc import doc
from django.shortcuts import redirect
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from django.utils.timezone import localtime

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from Gestion_Personnel_2 import settings
from administration.models import Administration
from connection.views import get_connected_user
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import os
from django.conf import settings

def generer_entete_pdf(p):
    """
    Ajoute l'entête du document PDF avec un logo centré (dimensions auto, ratio préservé)
    et des lignes de texte officielles.
    Retourne la position y restante pour le contenu à venir.
    """
    width, height = A4
    y = height - 60  # Position initiale en haut de la page
    line_height = 15

    administration = Administration.objects.first()
    if administration and administration.logo:
        logo_path = os.path.join(settings.MEDIA_ROOT, administration.logo.name)
        try:
            logo = ImageReader(logo_path)
            # Dimensions max souhaitées pour le logo
            max_logo_width = 120
            max_logo_height = 80
            
            # Récupérer taille réelle image
            img_width, img_height = logo.getSize()
            
            # Calcul du facteur d'échelle pour garder le ratio et ne pas dépasser max dimensions
            scale = min(max_logo_width / img_width, max_logo_height / img_height, 1)
            
            logo_width = img_width * scale
            logo_height = img_height * scale
            
            # Position horizontale centrée
            x = (width - logo_width) / 2
            # Position verticale : un peu en dessous du bord haut (y point de base en bas de l'image)
            y_logo = height - logo_height - 20
            
            p.drawImage(logo, x, y_logo, width=logo_width, height=logo_height, mask='auto')
            
            # Mise à jour de y sous l'image
            y = y_logo - 30
            
        except Exception as e:
            print(f"Erreur lors de l'affichage du logo : {e}")
            p.setFont("Times-Roman", 10)
            p.drawCentredString(width / 2, y, "Logo non disponible")
            y -= 40
    else:
        p.setFont("Times-Roman", 10)
        p.drawCentredString(width / 2, y, "Logo non disponible")
        y -= 40

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

    # Ajout d'une marge avant le contenu
    y -= 30

    return y

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

    # Assurez-vous que p est un objet canvas
    if isinstance(p, canvas.Canvas):
        p.setFont("Times-Roman", 10)
        p.drawString(x_offset_right, y_infos, f"Fait à Brazzaville, le {date_du_jour}")
        p.drawString(x_offset_right, y_infos - 100, f"{tnm} {tpm}")
    else:
        raise TypeError("L'objet p doit être un objet de type canvas.")

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
