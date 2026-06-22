# -*- coding: utf-8 -*-
"""
fonction_calcul_alpha.py — Modèle 2.2.

Calcule le coefficient alpha en utilisant des profils verticaux réalistes
pour chaque gaz à effet de serre (concentration variant avec l'altitude).
L'année n'est pas un paramètre : les concentrations de surface sont fixées
aux valeurs de référence 2026 codées dans Code_atmo_couche_backup.py.

Interprétation physique d'alpha :
  - alpha = flux sortant sommet atmosphère / flux émis par la surface
  - (1 - alpha) = fraction réabsorbée et renvoyée vers la surface (effet de serre)
"""
from . import Code_atmo_couche_backup as c_a


def calcul_alpha(P_emis):
    """
    Calcule alpha : fraction du flux IR de surface s'échappant vers l'espace.

    Parameters
    ----------
    P_emis : float
        Flux thermique émis par la surface [W m⁻²].

    Returns
    -------
    float
        alpha [-] : fraction du flux de surface qui traverse l'atmosphère.
    """
    flux_emis_terre = P_emis  # Flux émis par la surface [W m⁻²]

    # Simulation du transfert radiatif avec profils verticaux réalistes de chaque GES
    # (pas de paramètre d'année : concentrations de 2026 utilisées par défaut)
    lambda_range, z_range, upward_flux, optical_thickness, mean_flux_top = (
        c_a.simulate_radiative_transfer()
    )

    # alpha = flux sortant au sommet / flux émis par la surface
    # (1 - alpha) est réabsorbé par l'atmosphère et renvoyé vers la surface
    alpha = mean_flux_top / flux_emis_terre
    return alpha
