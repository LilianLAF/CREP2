# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 14:39:51 2025

@author: jeann
"""
from global_land_mask import globe
import requests
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import binned_statistic_2d

# ---------------------- Constantes capacité thermique ---------------------- #
RHO_W    = 1000.0   # kg/m³
RHO_BULK = 2600.0   # kg/m³ (sol)
CP_SEC   = 0.8      # kJ/kg/K (sol sec)
CP_WATER = 4.187    # kJ/kg/K (eau liquide)
CP_ICE   = 2.09     # kJ/kg/K (glace)
RHO_MER  = 1000.0   # kg/m³
RHO_GLACE = 917.0   # kg/m³

# ---------------------- Chargement RZSM (une seule fois) ---------------------- #
_RZSM_GRID = None
_RZSM_LAT_BINS = None
_RZSM_LON_BINS = None

def _load_rzsm():
    """
    Parameters
    ----------
    Aucun.

    Returns
    -------
    None
        Charge le CSV RZSM et remplit les grilles globales _RZSM_GRID,
        _RZSM_LAT_BINS, _RZSM_LON_BINS. Ne fait rien si déjà chargé.
    """
    global _RZSM_GRID, _RZSM_LAT_BINS, _RZSM_LON_BINS
    if _RZSM_GRID is not None:
        return
    # Donnees centralisees au niveau du groupe (dossier separe du code).
    csv_path = Path(__file__).parent.parent.parent / "donnees" / "Cp_humidity" / "average_rzsm_tout.csv"
    df = pd.read_csv(csv_path)
    df["lon"] = ((df["lon"] + 180) % 360) - 180
    lon_bins = np.arange(-180, 181, 1.0)
    lat_bins = np.arange(-90,   91, 1.0)
    statistic, _, _, _ = binned_statistic_2d(
        x=df["lon"], y=df["lat"], values=df["RZSM"],
        statistic="mean", bins=[lon_bins, lat_bins]
    )
    _RZSM_GRID = statistic.T
    _RZSM_LAT_BINS = lat_bins
    _RZSM_LON_BINS = lon_bins
    print("Données RZSM chargées.")

def _get_rzsm(lat, lon):
    """
    Parameters
    ----------
    lat : float
        Latitude [degrés].
    lon : float
        Longitude [degrés].

    Returns
    -------
    float
        Teneur en eau volumique du sol RZSM [-] au point le plus proche
        de la grille 1°×1°.
    """
    _load_rzsm()
    lat_idx = min(np.abs(_RZSM_LAT_BINS - lat).argmin(), _RZSM_GRID.shape[0] - 1)
    lon_idx = min(np.abs(_RZSM_LON_BINS - lon).argmin(), _RZSM_GRID.shape[1] - 1)
    return _RZSM_GRID[lat_idx, lon_idx]

def compute_cp_from_rzsm(rzsm: np.ndarray) -> np.ndarray:
    """Retourne Cp en kJ/kg/K depuis la teneur en eau volumique RZSM."""
    is_ice = np.isclose(rzsm, 0.9)
    rzsm_clipped = np.clip(rzsm, 1e-6, 0.999)
    w = (RHO_W * rzsm_clipped) / (RHO_BULK * (1 - rzsm_clipped) + RHO_W * rzsm_clipped)
    cp = CP_SEC + w * (CP_WATER - CP_SEC)
    return np.where(is_ice, CP_ICE, cp)

# ---------------------- Détection biome + capacité ---------------------- #
def classify_point(lon, lat):
    """Renvoie (Cp_massique kJ/kg/K, rho kg/m³) selon le type de surface."""
    if abs(lat) > 75:
        return CP_ICE, RHO_GLACE  # Glace polaire
    if not globe.is_land(lat, lon):
        return CP_WATER, RHO_MER  # Océan
    # Sol terrestre : Cp calculée depuis l'humidité réelle (RZSM)
    rzsm = _get_rzsm(lat, lon)
    if np.isnan(rzsm):
        cp_kj = CP_SEC
    else:
        cp_kj = float(compute_cp_from_rzsm(np.array([rzsm]))[0])
    return cp_kj, RHO_BULK

def masse_volumique_point(lon, lat):
    """Renvoie la masse volumique (float) en kg/m³."""
    _, rho = classify_point(lon, lat)
    return rho

# ---------------------- API NASA POWER pour l’albédo ---------------------- #
def get_mean_albedo(lat, lon, start="20220101", end="20231231"):
    """
    Parameters
    ----------
    lat : float
        Latitude [degrés].
    lon : float
        Longitude [degrés].
    start : str, optional
        Date de début au format YYYYMMDD. The default is "20220101".
    end : str, optional
        Date de fin au format YYYYMMDD. The default is "20231231".

    Returns
    -------
    float
        Albédo moyen [-] calculé à partir du rapport flux montant / flux
        descendant (NASA POWER). Retourne 0.3 en cas d'erreur.
    """
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
    
    #altitude surface (via coordonnées)
def get_altitude(lat, lon):
    """Récupère l'altitude d'un point via l'API Open-Elevation.Lève une erreur explicite si le réseau ou l'API ne répond pas.  """
    url = "https://api.open-elevation.com/api/v1/lookup"
    params = {"locations": f"{lat},{lon}"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "results" in data and data["results"]:
            return float(data["results"][0].get("elevation", 0.0))
        else:
            raise ValueError("Données d'altitude introuvables dans la réponse de l'API.")

    except requests.exceptions.ConnectionError:
        # Cas spécifique où Internet/DNS ne répond pas (ton erreur NameResolutionError)
        raise ConnectionError(
            "\n[Erreur Réseau] Impossible de se connecter à l'API Open-Elevation.\n"
            "Vérifie ta connexion internet, ton VPN ou ton pare-feu (firewall)."
        )
    except Exception as e:
        # Pour toute autre erreur (timeout, HTTP 500, etc.)
        raise RuntimeWarning(f"Erreur lors de la récupération de l'altitude : {e}")