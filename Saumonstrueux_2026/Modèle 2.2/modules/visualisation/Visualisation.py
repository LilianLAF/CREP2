import datetime
import sys
import os
import pandas as pd
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from bilan_energetique import librairie_puissances as l_p
from bilan_energetique import parametrage_surface as p_s
from bilan_energetique import parametrage_convection as p_c
from atmosphere import fonction_calcul_alpha as f_c


def Visualiation(T_point, annee, lat, long):
    resultats_dir = Path(__file__).parent.parent.parent / "resultats"
    date_debut = datetime.datetime(annee, 1, 1)
    dates = [date_debut + datetime.timedelta(hours=i) for i in range(len(T_point))]

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(dates, T_point)

    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)

    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    plt.xlabel("Date")
    plt.ylabel("Température (K)")
    plt.title(f"Température pour un point de coordonnées ({lat}°N, {long}°E)")
    plt.grid(True)
    plt.tight_layout()
    nom_fichier = f"temperature_{lat}N_{long}E_{annee}.png"
    plt.savefig(resultats_dir / nom_fichier, dpi=150)
    print(f"Graphique sauvegardé : {nom_fichier}")

    #génère un tableau de valeurs a sauvegarder
    dates = [datetime.datetime(annee, 1, 1) + datetime.timedelta(hours=i) for i in range(len(T_point))]
    df = pd.DataFrame({"Date": dates, "Température (K)": T_point})
    df.to_csv(resultats_dir / f"temperature_{lat}N_{long}E_{annee}.csv", index=False)
    print(f"Tableau de valeurs sauvegardé : temperature_{lat}N_{long}E_{annee}.csv")