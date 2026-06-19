# -*- coding: utf-8 -*-

import datetime
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "modules"))

import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import librairie_puissances as l_p
import parametrage_surface as p_s
import parametrage_convection as p_c
import fonction_calcul_alpha as f_c
import Visualisation as Visu

# ---------------------- Simulation Température ---------------------- #
def temp(lat = 48.85, long = 2.35):
    """
    Parameters
    ----------
    lat : float, optional
        Latitude du point [degrés]. Par défaut 48.85.
    long : float, optional
        Longitude du point [degrés]. Par défaut 2.35.

    Returns
    -------
    list of float
        Série temporelle de température de surface [K] sur une année,
        pas horaire (8761 valeurs).
    """
    cm, rho = p_s.classify_point(long, lat)
    cm = cm * 1000.0  # Conversion kJ/kg/K → J/kg/K
    A = p_s.get_mean_albedo(lat, long)
    h = p_c.liste_h(lat,long)
    alpha = f_c.calcul_alpha(5.67e-8*(288)**4, annee)
    d = 0.1 #10cm
    S = 1 #surface
    c = cm*rho*S*d
    T0 = 283
    T_air = 283
    T = [T0]
    
    #A modifier pour la discrétisation :
    dt = 3600  
    # a modifier pour le temps de simulation
    Duree_Siumlation = 24*365 

    for i in range(Duree_Siumlation):
        
        if i % (Duree_Siumlation // 20) == 0:                                              # Barre de chargment
            pct = int(100 * i / Duree_Siumlation)                                          #
            barre = '█' * (pct // 5) + '░' * (20 - pct // 5)                               #
            print(f"\r  Simulation température : [{barre}] {pct:3d}%", end='', flush=True) #
        
        P_emis = l_p.P_em_surf_thermal(lat,long,i,T[i]) + l_p.P_em_surf_conv(lat,long,i, T[i], T_air, h[i]) + l_p.P_em_surf_evap(lat,long,i)
        P_recue = l_p.P_abs_surf_solar(lat,long,i,A) + l_p.P_em_atm_thermal_down(lat, long,i, alpha, P_emis) 
        dT = dt * (P_recue - P_emis) / c
        T.append(T[i] + dT)
    
    print(f"\r  Simulation température : [{'█'*20}] 100%") # Barre de chargment
    
    return T

if __name__ == "__main__":
    # Simulation température
    lat = float(input("Indiquez la latitude du lieu : " ))
    long = float(input("Indiquez la longitude du lieu : "))
    annee = int(input("Indiquez l'année choisie : "))
    T_point = temp(lat, long)
    #altitude_sol=p_s.get_altitude(lat,long)

    Visu.Visualiation(T_point, annee, lat, long)
    