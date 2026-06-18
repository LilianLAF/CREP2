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

    taux_co2_ppm = concentration_CO2(annee)#en ppm
    taux_o3_ppm = concentration_O3(annee)#en ppm
    taux_n2o_ppm = concentration_N2O(annee)#en ppm
    taux_ch4_ppm = concentration_CH4(annee)#en ppm
    taux_h2o_ppm = concentration_H2O(annee)#en ppm

    lambda_range, z_range, upward_flux, optical_thickness, mean_flux_top = c_a.simulate_radiative_transfer(taux_co2_ppm, taux_o3_ppm, taux_n2o_ppm, taux_ch4_ppm, taux_h2o_ppm)
    
    alpha = mean_flux_top/flux_emis_terre
    
    return(alpha)
