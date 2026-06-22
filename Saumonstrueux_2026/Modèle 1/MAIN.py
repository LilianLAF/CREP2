# -*- coding: utf-8 -*-
"""
MAIN.py — Modèle 1 : bilan énergétique avec alpha constant (CO₂ uniquement, concentration fixe).

Lancement : python MAIN.py  (depuis le dossier Modèle 1/)
Sortie : graphique + CSV dans resultats/
"""

import datetime
import sys
import os

# Ajoute le dossier modules/ au chemin de recherche Python
# pour que les sous-paquets bilan_energetique/, atmosphere/ et visualisation/ soient trouvables
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "modules"))

import matplotlib
matplotlib.use('Agg')  # Moteur non-interactif : génère les fichiers PNG sans afficher de fenêtre
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# Importation des sous-modules du projet
from bilan_energetique import librairie_puissances as l_p   # Calculs des flux énergétiques
from bilan_energetique import parametrage_surface as p_s    # Caractéristiques thermiques de la surface
from bilan_energetique import parametrage_convection as p_c  # Coefficient de convection via le vent
from atmosphere import fonction_calcul_alpha as f_c          # Coefficient alpha (transfert radiatif IR)
from visualisation import Visualisation as Visu              # Tracé et sauvegarde des résultats


# ─────────────────────────────────────────────────────────────────────
# FONCTION PRINCIPALE DE SIMULATION
# ─────────────────────────────────────────────────────────────────────
def temp(lat=48.85, long=2.35):
    """
    Simule l'évolution temporelle de la température de surface sur une année.

    Méthode : bilan énergétique discret, schéma d'Euler explicite à pas horaire.
    L'équation résolue est :  c × dT/dt = P_recue − P_emis
    où c est la capacité thermique volumique de la couche de sol active.

    Parameters
    ----------
    lat : float
        Latitude du point simulé [degrés].
    long : float
        Longitude du point simulé [degrés].

    Returns
    -------
    list of float
        Série temporelle de température [K] (8761 valeurs, pas horaire).
    """
    # --- Paramètres de surface ---
    cm, rho = p_s.classify_point(long, lat)  # Cp massique [kJ/kg/K] et masse volumique [kg/m³]
    cm = cm * 1000.0       # Conversion kJ/kg/K → J/kg/K
    A = p_s.get_mean_albedo(lat, long)        # Albédo moyen [-] récupéré via NASA POWER
    h = p_c.liste_h(lat, long)                # Liste des 8760 coefficients de convection horaires [W/m²/K]

    # --- Coefficient alpha ---
    # alpha = fraction du flux IR de surface qui s'échappe vers l'espace
    # (1 - alpha) est réabsorbé par l'atmosphère et renvoyé vers la surface (effet de serre)
    # Dans le Modèle 1, alpha est calculé une seule fois avec la concentration CO₂ de l'année choisie
    alpha = f_c.calcul_alpha(5.67e-8 * (288)**4, annee)

    # --- Paramètres thermiques de la colonne de sol ---
    d = 0.39   # Profondeur de la couche active [m] (39 cm, cf. Ex.1 Chap.11 de 2A)
    S = 1      # Surface unitaire [m²]
    c = cm * rho * S * d  # Capacité thermique totale de la colonne [J/K]

    # --- Conditions initiales ---
    T0 = 283      # Température initiale de surface [K] (~10°C)
    T_air = 283   # Température de l'air (supposée constante) [K]
    T = [T0]      # Liste des températures simulées

    # --- Discrétisation temporelle ---
    dt = 3600              # Pas de temps [s] = 1 heure
    Duree_Siumlation = 24 * 365  # Nombre de pas = 1 an

    # --- Boucle de simulation (schéma d'Euler explicite) ---
    for i in range(Duree_Siumlation):
        # Flux émis par la surface : rayonnement thermique + convection + évaporation
        P_emis = (l_p.P_em_surf_thermal(lat, long, i, T[i])
                  + l_p.P_em_surf_conv(lat, long, i, T[i], T_air, h[i])
                  + l_p.P_em_surf_evap(lat, long, i))

        # Flux reçu par la surface : solaire absorbé + IR atmosphérique redescendu
        P_recue = (l_p.P_abs_surf_solar(lat, long, i, A)
                   + l_p.P_em_atm_thermal_down(lat, long, i, alpha, P_emis))

        # Variation de température : c × ΔT = (P_recue − P_emis) × dt
        dT = dt * (P_recue - P_emis) / c
        T.append(T[i] + dT)

    return T


# ─────────────────────────────────────────────────────────────────────
# POINT D'ENTRÉE
# ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Saisie interactive des paramètres de simulation
    lat = float(input("Indiquez la latitude du lieu : "))
    long = float(input("Indiquez la longitude du lieu : "))
    annee = int(input("Indiquez l'année choisie : "))

    # Lancement de la simulation
    T_point = temp(lat, long)

    # Sauvegarde du graphique et du CSV dans resultats/
    Visu.Visualiation(T_point, annee, lat, long)
    