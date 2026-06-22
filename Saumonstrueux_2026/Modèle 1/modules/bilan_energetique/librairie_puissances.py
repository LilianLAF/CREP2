#Cette librairie propose une convention pour le nom des puissances surfaciques considérées, mais n'a pas vocation à être réutilisée telle quelle.
# conventions:
# lat: float (radian), 0 is at equator, -pi/2 is at south pole, and +pi/2 is at north pole
# long: float (radian), 0 is at greenwich meridiant
# t: float (s), 0 is at 00:00 (greenwich time) january 1, 365*24*60*60 is at the end of the year, (maybe use 365.25? no idea what is best, or maybe use UTC ?)


import numpy as np
import math
import pathlib
from atmosphere import fonction_calcul_alpha as f_c
P0 = 1360  # W/m² – zenith irradiance at the top of the atmosphere
PHI = 0.409  # precession angle rad  (23.45 deg)
SIGMA = 5.67e-8  # W/m²K⁴ – Stefan-Boltzmann constant
S = 1 #surface

import numpy as np
import math
import pathlib
from atmosphere import fonction_calcul_alpha as f_c

# --- AJOUTE CE BLOC ICI ---
try:
    import geopandas as gpd
    from shapely.geometry import Point
    GEOPANDAS_AVAILABLE = True
except ImportError:
    print("AVERTISSEMENT: GeoPandas non trouvé. La détection des continents sera désactivée.")
    GEOPANDAS_AVAILABLE = False
# --------------------------
# ────────────────────────────────────────────────
# DÉTECTION DE CONTINENT
# ────────────────────────────────────────────────
SHAPEFILE_PATH = (
    pathlib.Path(__file__).resolve().parent.parent.parent.parent
    / "donnees"
    / "map"
    / "ne_110m_admin_0_countries.shp"
)


def create_continent_finder(shapefile_path: pathlib.Path):
    """
    Crée une fonction qui trouve le continent pour un point (lat, lon).

    IN:
        shapefile_path (pathlib.Path): Chemin vers le fichier shapefile des pays.

    OUT:
        function: Une fonction qui prend (lat, lon) et retourne un nom de continent.
    """
    if not GEOPANDAS_AVAILABLE:
        return lambda lat, lon: "Océan"
    try:
        world = gpd.read_file(shapefile_path).to_crs(epsg=4326)
    except Exception as e:
        print(f"AVERTISSEMENT: Impossible de charger le shapefile: {e}")
        return lambda lat, lon: "Océan"

    def find_continent_for_point(lat: float, lon: float) -> str:
        point = Point(lon, lat)
        valid_world = world[world.geometry.notna()]
        for _, row in valid_world.iterrows():
            if row["geometry"].contains(point):
                return row["CONTINENT"]
        return "Océan"

    return find_continent_for_point


# Instance globale de la fonction de détection, créée une seule fois.
continent_finder = create_continent_finder(SHAPEFILE_PATH)

# ────────────────────────────────────────────────
# DONNÉES DE CHALEUR LATENTE (Q) VIA ÉVAPORATION
# ────────────────────────────────────────────────
Delta_hvap = 2453000  # Enthalpie de vaporisation de l'eau [J kg⁻¹]
rho_eau = 1000  # Masse volumique de l'eau [kg m⁻³]
Delta_t_an = 365.25 * 24 * 3600  # Durée d'une année en secondes [s]

# Taux d'évaporation moyens par continent [m an⁻¹], convertis en [m s⁻¹]
evap_Eur = 0.49 / Delta_t_an
evap_Am_Nord = 0.47 / Delta_t_an
evap_Am_sud = 0.94 / Delta_t_an
evap_oceanie = 0.41 / Delta_t_an
evap_Afr = 0.58 / Delta_t_an
evap_Asi = 0.37 / Delta_t_an
evap_ocean = 1.40 / Delta_t_an

# Flux de chaleur latente correspondants [W m⁻²]
Q_LATENT_CONTINENT = {
    "Europe": Delta_hvap * rho_eau * evap_Eur,
    "North America": Delta_hvap * rho_eau * evap_Am_Nord,
    "South America": Delta_hvap * rho_eau * evap_Am_sud,
    "Oceania": Delta_hvap * rho_eau * evap_oceanie,
    "Africa": Delta_hvap * rho_eau * evap_Afr,
    "Asia": Delta_hvap * rho_eau * evap_Asi,
    "Océan": Delta_hvap * rho_eau * evap_ocean,
    "Antarctica": 0.0,  # Pas d'évaporation en Antarctique
}



def P_inc_solar(lat: float, lon: float, t: float):
    S0 = 1361  # constante solaire
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    inclinaison = np.radians(23.5)

    # Convertir l’instant t (en heures) en jour et heure
    t_int = math.ceil(t)
    jour = t_int // 24 + 1  # jour entre 1 et 365
    heure = t_int % 24      # heure entre 0 et 23

    # Calcul des paramètres solaires à ce moment précis
    declinaison = np.arcsin(
        np.sin(inclinaison) * np.sin(2 * np.pi * (jour - 81) / 365)
    )
    soleil = np.array([np.cos(declinaison), 0, np.sin(declinaison)])
    soleil /= np.linalg.norm(soleil)

    angle_terre = np.radians(15 * (heure - 12))
    x = np.cos(lat_rad) * np.cos(lon_rad + angle_terre)
    y = np.cos(lat_rad) * np.sin(lon_rad + angle_terre)
    z = np.sin(lat_rad)
    normale = np.array([x, y, z])

    prod = np.dot(normale, soleil)
    return max(0, S0 * prod)

# Surface
def P_abs_surf_solar(lat: float, long: float, t: float, A):
    puissance_abs_surf_solar = (1 - A)* P_inc_solar(lat, long, t) * S
    return puissance_abs_surf_solar


def P_em_surf_thermal(lat: float, long: float, t: float, T: float):
    return SIGMA * (T**4)


def P_em_surf_conv(lat: float, long: float, t: float, T, T_air,h):
    return h * S * (T - T_air)

#def P_em_surf_evap(lat: float, long: float, t: float):
#    return 86
def P_em_surf_evap(lat: float, lon: float, t: float = 0, verbose: bool = False) -> float:
    """
    Récupère la valeur du flux de chaleur latente (Q) pour un point géographique.

    IN:
        lat (float): Latitude [degrés].
        lon (float): Longitude [degrés].
        verbose (bool): Si True, affiche le continent détecté.

    OUT:
        float: Flux de chaleur latente de base [W m⁻²].
    """
    continent = continent_finder(lat, lon)
    q_val = Q_LATENT_CONTINENT.get(continent, Q_LATENT_CONTINENT["Océan"])

    if verbose:
        print(
            f"Coordonnées ({lat:.2f}, {lon:.2f}) détectées sur : "
            f"{continent} (Q base = {q_val:.2f} W m⁻²)"
        )

    # Heuristique pour les zones polaires glacées
    if lat > 75:
        return 0.0
    return q_val


# atmosphere
def P_abs_atm_solar(lat: float, long: float, t: float, Pinc: float):
    AbsAtmo = 0.22
    return AbsAtmo * Pinc


def P_abs_atm_thermal(lat: float, long: float, t: float, T: float):
    return 358


def P_em_atm_thermal_up(lat: float, long: float, t: float, alpha, P_emis):
    return (alpha)*P_emis

def P_em_atm_thermal_down(lat: float, long: float, t: float, alpha, P_emis):
    return (1-alpha)*P_emis
