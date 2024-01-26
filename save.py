import pandas as pd
import os


def supprimer_tous_les_fichiers(dossier):
    for nom in os.listdir(dossier):
        chemin = os.path.join(dossier, nom)
        if os.path.isfile(chemin):
            os.remove(chemin)

def save_infos(name_project, titre) : 
    df = pd.read_csv('titres.csv')
    new_row = pd.DataFrame({'vod_name': [name_project+".mp4"], 'titre': [titre]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv('titres.csv', index=False)
    supprimer_tous_les_fichiers('temporaire/')




import matplotlib.pyplot as plt
import matplotlib.patches as patches

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def diviser_appartement(longueur, largeur):
    fig, ax = plt.subplots()

    # Contraintes
    surface_piece1 = 9  # m²
    largeur_piece2 = 5  # m

    # Calculer les dimensions des pièces en respectant les contraintes
    # Hypothèse : les pièces sont rectangulaires
    largeur_piece1 = largeur_piece2
    longueur_piece1 = surface_piece1 / largeur_piece1

    # Positionner la pièce 1
    piece1 = patches.Rectangle((0, 0), longueur_piece1, largeur_piece1, edgecolor='blue', facecolor='none')
    ax.add_patch(piece1)

    # Positionner la pièce 2
    longueur_piece2 = min(longueur - longueur_piece1, largeur)
    piece2 = patches.Rectangle((longueur_piece1, 0), longueur_piece2, largeur_piece2, edgecolor='red', facecolor='none')
    ax.add_patch(piece2)

    # Le reste de l'espace est le salon
    salon = patches.Rectangle((0, largeur_piece1), longueur, largeur - largeur_piece1, edgecolor='green', facecolor='none')
    ax.add_patch(salon)

    # Configurer l'affichage
    ax.set_xlim([0, longueur])
    ax.set_ylim([0, largeur])
    ax.set_title('Disposition des pièces')
    ax.set_xlabel('Longueur (m)')
    ax.set_ylabel('Largeur (m)')

    plt.show()

# Exemple d'utilisation
diviser_appartement(10, 8)
