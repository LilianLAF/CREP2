# -*- coding: utf-8 -*-
import code_atmo_couche_backup as c_a

def concentration_CO2(annee):
    """
    Renvoie la concentration estimée de CO₂ en ppm pour une année donnée.
    """
    if 1838 <= annee <= 1972:
        return 0.294 * annee - 262
    elif annee < 1838:
        return 278  # valeur moyenne avant l'ère industrielle
    else:
        return 1.9 * annee - 3430  # modèle linéaire post-1952

def concentration_CO2_altitude_annee(altitude, annee):
    """
    Renvoie la proportion de CO₂ en ppm pour une altitude et une année données.
    Combine le profil altitudinal (référence 2000) et l'évolution temporelle.
    """
    if 0 <= altitude <= 60:
        prop_altitude = 380
    elif altitude > 132:
        prop_altitude = 0
    else:
        prop_altitude = -5.26 * altitude + 736
    coef = concentration_CO2(annee) / concentration_CO2(2000)
    return prop_altitude * coef

    
def concentration_O3(annee):
    return 

def concentration_N2O(annee):
    return

def concentration_CH4(annee):
    return

def concentration_H2O(annee):
    return

def calcul_alpha(P_emis, annee):
    flux_emis_terre = P_emis #en W/m^2

    taux_o3 = concentration_O3(annee)
    taux_n2o = concentration_N2O(annee)
    taux_ch4 = concentration_CH4(annee)
    taux_h2o = concentration_H2O(annee)

    lambda_range, z_range, upward_flux, optical_thickness = c_a.simulate_radiative_transfer(annee, taux_o3, taux_n2o, taux_ch4, taux_h2o)

    mean_flux_top = upward_flux[-1, :].sum()
    alpha = mean_flux_top / flux_emis_terre

    return alpha
