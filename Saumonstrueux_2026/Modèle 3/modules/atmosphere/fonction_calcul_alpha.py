# -*- coding: utf-8 -*-
"""
fonction_calcul_alpha.py — Modèle 3 (modèle le plus complet).

Calcule le coefficient alpha en combinant :
  - des profils verticaux réalistes de chaque GES (variation avec l'altitude)
  - des concentrations de surface dépendant de l'année simulée

Interprétation physique d'alpha :
  - alpha = flux sortant sommet atmosphère / flux émis par la surface
  - alpha proche de 1 : atmosphère transparente (peu d'effet de serre)
  - alpha proche de 0 : fort effet de serre
  - (1 - alpha) est réabsorbé par l'atmosphère et renvoyé vers la surface
"""
from . import Code_atmo_couche_backup as c_a


def calcul_alpha(P_emis, annee):
    """
    Calcule alpha : fraction du flux IR de surface s'échappant vers l'espace.

    Parameters
    ----------
    P_emis : float
        Flux thermique émis par la surface terrestre [W m⁻²].
    annee : int
        Année simulée (détermine les concentrations des gaz à effet de serre).

    Returns
    -------
    float
        Coefficient alpha [-] : fraction du flux de surface qui s'échappe
        vers l'espace (1 - alpha est réabsorbé par l'atmosphère).
    """
    flux_emis_terre = P_emis  # Flux émis par la surface [W m⁻²]

    # Simulation complète du transfert radiatif (année + profils verticaux)
    # Retourne le flux total au sommet de l'atmosphère intégré spectralement [W m⁻²]
    lambda_range, z_range, upward_flux, optical_thickness, mean_flux_top = (
        c_a.simulate_radiative_transfer(annee)
    )

    # Définition d'alpha : rapport entre le flux sorti et le flux initial
    # Exemple typ. 2026 : alpha ≈ 0.6 → environ 40 % du flux de surface est retenu par l'atmosphère
    alpha = mean_flux_top / flux_emis_terre
    return alpha
