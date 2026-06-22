# -*- coding: utf-8 -*-
"""
fonction_calcul_alpha.py — Modèle 1.

Calcule le coefficient alpha = fraction du flux IR de surface qui s'échappe
vers l'espace, en fonction de la concentration en CO₂ de l'année simulée.

Seul le CO₂ est pris en compte dans ce modèle (pas de CH₄, N₂O, O₃, H₂O).
Sa concentration est uniforme sur toute la colonne atmosphérique.

Interprétation physique d'alpha :
  - alpha proche de 1 : atmosphère transparente, peu d'effet de serre
  - alpha proche de 0 : atmosphère très absorbante, fort effet de serre
  Dans la boucle de simulation : P_reçue += (1-alpha) × P_emis
"""
from . import transfert_radiatif as c_a


def concentration_CO2(annee):
    """
    Renvoie la concentration de CO₂ en ppm pour une année donnée.

    Modèle empirique par morceaux :
      - avant 1838 : 278 ppm (valeur pré-industrielle)
      - 1838–1972 : croissance linéaire lente
      - après 1972 : accélération linéaire (combustibles fossiles)
    """
    if 1838 <= annee <= 1972:
        return 0.294 * annee - 262
    elif annee < 1838:
        return 278        # Concentration pré-industrielle moyenne [ppm]
    else:
        return 1.9 * annee - 3430  # Croissance accélérée post-1972


def calcul_alpha(P_emis, annee):
    """
    Calcule alpha : fraction du flux IR de surface s'échappant vers l'espace.

    Parameters
    ----------
    P_emis : float
        Flux thermique émis par la surface [W m⁻²].
    annee : int
        Année simulée (détermine la concentration CO₂).

    Returns
    -------
    float
        alpha [-] : fraction du flux de surface qui traverse l'atmosphère.
    """
    # Conversion de la concentration annuelle de CO₂ en fraction volumique [-]
    taux_co2 = concentration_CO2(annee)
    taux_co2_ppm = taux_co2 * 1e-6  # ppm → fraction sans dimension

    # Simulation du transfert radiatif : le flux IR monte de la surface vers le sommet
    # Seul paramètre : la fraction volumique de CO₂ (uniforme sur toute la colonne)
    lambda_range, z_range, upward_flux, optical_thickness, earth_flux = (
        c_a.simulate_radiative_transfer(taux_co2_ppm)
    )

    # Flux total [W m⁻²] parvenant au sommet de l'atmosphère (intégration spectrale)
    mean_flux_top = upward_flux[-1, :].sum()

    flux_emis_terre = P_emis  # Flux émis par la surface [W m⁻²]

    # Définition d'alpha : rapport flux sortant / flux de surface
    # alpha = 1 → pas d'absorption atmosphérique (pas d'effet de serre)
    # alpha < 1 → une fraction (1-alpha) est réabsorbée et réémise vers la surface
    alpha = mean_flux_top / flux_emis_terre
    return alpha
