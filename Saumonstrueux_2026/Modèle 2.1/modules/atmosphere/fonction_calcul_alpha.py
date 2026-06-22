# -*- coding: utf-8 -*-
from . import Code_atmo_couche_backup as c_a

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
    
def concentration_CH4(annee):
    """
    Renvoie la concentration estimée de CH_4 en ppm pour une année donnée.
    """
    if 1786 <= annee:
        return 675/1000 #(en ppm)
    else:
        return (5.07*annee-8.38*1000)/1000  # valeur moyenne avant l'ère industrielle
    
def concentration_N2O(annee):
    if 1836 <= annee <= 1966:
        return (0.237 * annee - 172)/1000 #(en ppm)
    elif annee < 1836:
        return 263/1000  # valeur moyenne avant l'ère industrielle
    else:
        return (0.77 * annee - 1.22*1000)/1000 
 
def concentration_03(annee):
    return 9 #(en ppm) 

def concentration_H2O(annee):
    return 400

def calcul_alpha(P_emis, annee):
    taux_CO2 = concentration_CO2(annee) * 1e-6 # convertir en fraction
    taux_CH4 = concentration_CH4(annee) * 1e-6  
    taux_N2O = concentration_N2O(annee) * 1e-6  
    taux_O3 = concentration_03(annee) * 1e-6    
    taux_H2O = concentration_H2O(annee) * 1e-6
    
    lambda_rxange, z_range, upward_flux, optical_thickness, earth_flux = c_a.simulate_radiative_transfer(taux_CO2, taux_CH4, taux_N2O, taux_O3, taux_H2O)
    mean_flux_top = upward_flux[-1,:].sum()
    flux_emis_terre = P_emis #en W/m^2
    alpha = mean_flux_top/flux_emis_terre
    return(alpha)
