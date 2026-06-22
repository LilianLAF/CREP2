# -*- coding: utf-8 -*-
import code_atmo_couche_backup as c_a


def calcul_alpha(P_emis, annee):
    """
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
    flux_emis_terre = P_emis #en W/m^2

    lambda_range, z_range, upward_flux, optical_thickness, mean_flux_top = c_a.simulate_radiative_transfer(annee)

    alpha = mean_flux_top / flux_emis_terre

    return alpha
