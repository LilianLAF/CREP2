# -*- coding: utf-8 -*-

import datetime
import sys
import os
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import librairie_puissances as l_p
import Visualisation as Visu

# ---------------------- Simulation Température ---------------------- #
def temp(lat = 48.85, long = 2.35):
    cm, rho = 4180, 1000   # kJ/kg/K, kg
    alpha = 2
    d = 0.39 #en cm
    P0 = 1360  # W/m² – zenith irradiance at the top of the atmosphere
    PHI = 0.409  # precession angle rad  (23.45 deg)
    SIGMA = 5.67e-8  # W/m²K⁴ – Stefan-Boltzmann constant
    A=0.31
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
        P_emis = l_p.P_em_surf_thermal(lat,long,i,T[i]) + l_p.P_em_surf_conv(lat,long,i, T[i], T_air, h= None) + l_p.P_em_surf_evap(lat,long,i)
        P_recue = l_p.P_abs_surf_solar(lat,long,i,A) + l_p.P_em_atm_thermal_down(lat, long,i, alpha, P_emis) 
        dT = dt * (P_recue - P_emis) / c
        T.append(T[i] + dT)
    
    return T

if __name__ == "__main__":
    # Simulation température
    lat = float(input("Indiquez la latitude du lieu : " ))
    long = float(input("Indiquez la longitude du lieu : "))
    annee = int(input("Indiquez l'année choisie : "))
    T_point = temp(lat, long)
    

    Visu.Visualiation(T_point, annee, lat, long)
    