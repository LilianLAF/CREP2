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
    cm, rho = p_s.classify_point(long, lat)
    cm = cm * 1000.0  # Conversion kJ/kg/K → J/kg/K
    A = p_s.get_mean_albedo(lat, long)
    h = p_c.liste_h(lat,long)
    alpha = f_c.calcul_alpha(5.67e-8*(288)**4)
    d = 0.39 #39cm cf ex 1 chap 11 de 2A
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
        P_emis = l_p.P_em_surf_thermal(lat,long,i,T[i]) + l_p.P_em_surf_conv(lat,long,i, T[i], T_air, h[i]) + l_p.P_em_surf_evap(lat,long,i)
        P_recue = l_p.P_abs_surf_solar(lat,long,i,A) + l_p.P_em_atm_thermal_down(lat, long,i, alpha, P_emis) 
        dT = dt * (P_recue - P_emis) / c
        T.append(T[i] + dT)
    
    return T

if __name__ == "__main__":
    # Simulation température
    lat = float(input("Indiquez la latitude du lieu : " ))
    long = float(input("Indiquez la longitude du lieu : "))
    T_point = temp(lat, long)
    #altitude_sol=p_s.get_altitude(lat,long)

    Visu.Visualiation(T_point,2026, lat, long)
    