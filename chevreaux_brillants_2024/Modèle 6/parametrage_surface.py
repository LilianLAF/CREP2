# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 14:39:51 2025

@author: jeann
"""
from global_land_mask import globe
import requests

def get_altitude(lat, lon):
    """Récupère l'altitude (en mètres) du point via Open-Elevation."""
    url = "https://api.open-elevation.com/api/v1/lookup"
    params = {"locations": f"{lat},{lon}"}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data["results"][0]["elevation"])
    except Exception as e:
        print("Erreur lors de la récupération de l'altitude :", e)
        return 0.0

def classify_point(lon, lat):
    """Renvoie la capacité thermique massique (int)"""
    if abs(lat) > 75:
        return 2060  # Glace
    if globe.is_land(lat, lon):
        return 1046  # Terre
    else:
        return 4180  # Mer

def masse_volumique_point(lon, lat):
    """Renvoie la masse volumique (int) en kg/m³"""
    if abs(lat) > 75:
        return 917  # Glace
    if globe.is_land(lat, lon):
        return 2600  # Terre
    else:
        return 1000  # Mer

# ---------------------- API NASA POWER pour l’albédo ---------------------- #
def get_mean_albedo(lat, lon, start="20220101", end="20231231"):
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN,ALLSKY_SFC_SW_UP",
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
        allsky = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
        upsky = data['properties']['parameter']['ALLSKY_SFC_SW_UP']

        albedo_values = [
            upsky[day] / allsky[day]
            for day in allsky if allsky[day] > 0 and upsky[day] is not None
        ]
        return sum(albedo_values) / len(albedo_values) if albedo_values else 0.3
    except Exception as e:
        print("Erreur lors de la récupération de l'albédo :", e)
        return 0.3