# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 15:10:53 2025

@author: jeann
"""
import requests
# ---------------------- Convection par vitesse de vent ---------------------- #
import math

def rho_air(alt):
    """Densité de l'air en kg/m^3 selon l'altitude (barométrique)."""
    P0 = 101325.0
    T0 = 288.15
    g = 9.80665
    M = 0.0289644
    R = 8.31447
    lapse_rate = 0.0065
    if alt < 0:
        alt = 0
    # Pression en Pa suivant le modèle barométrique isotherme avec gradient thermique
    P = P0 * (1 - lapse_rate * alt / T0) ** ((g * M) / (R * lapse_rate))
    return P * M / (R * (T0 - lapse_rate * alt))
def coefficient_convection(v, alt=0):
    rho = rho_air(alt)
    mu = 1.8e-5       # Viscosité dynamique de l'air (Pa·s)
    L = 1.0           # Longueur caractéristique (m)
    Pr = 0.71         # Nombre de Prandtl pour l'air
    lambda_air = 0.026  # Conductivité thermique de l'air (W/m·K)

    Re = rho * v * L / mu
    if Re < 5e5:
        C, m, n = 0.664, 0.5, 1/3
    else:
        C, m, n = 0.037, 0.8, 1/3

    Nu = C * Re**m * Pr**n
    h = Nu * lambda_air / L
    return h

# ---------------------- API Nasa pour le vent ---------------------- #
def get_daily_wind_speed(lat, lon, start="20240101", end="20241231"):
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "WS2M",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start,
        "end": end,
        "format": "JSON"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        wind_data = data["properties"]["parameter"]["WS2M"]
        wind_values = [wind_data[day] for day in sorted(wind_data)]
        return wind_values  # Liste de 365 vitesses moyennes journalières
    except Exception as e:
        print("Erreur lors de la récupération du vent :", e)
        return [2.5] * 365  # Valeur par défaut

def liste_h (lat,long):
    L = []
    v = get_daily_wind_speed(lat, long)
    for i in range(365):
        for j in range (24):
            L.append(coefficient_convection(v[i], alt))
    return(L)