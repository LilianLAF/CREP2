# -*- coding: utf-8 -*-
from . import Code_atmo_couche_backup as c_a


def calcul_alpha(P_emis):
    flux_emis_terre = P_emis #en W/m^2

    lambda_range, z_range, upward_flux, optical_thickness, mean_flux_top = c_a.simulate_radiative_transfer()

    alpha = mean_flux_top / flux_emis_terre

    return alpha
