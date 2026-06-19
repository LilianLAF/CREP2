import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------

# ===================
# BLACKBODY RADIATION
# ===================

def planck_function(lambda_wavelength, T):
    """
    Parameters
    ----------
    lambda_wavelength : float or np.ndarray
        Longueur d'onde [m].
    T : float
        Température du corps noir [K].

    Returns
    -------
    float or np.ndarray
        Luminance spectrale du corps noir [W m⁻² m⁻¹ sr⁻¹].
    """
    h = 6.62607015e-34      # Planck's constant, J*s
    c = 2.998e8             # Speed of light, m/s
    kB = 1.380649e-23       # Boltzmann's constant, J/K
    term1 = (2 * h * c**2) / lambda_wavelength**5
    term2 = np.exp((h * c) / (lambda_wavelength * kB * T)) - 1
    return term1 / term2

# ----------------------------------------------------------------------------------------------------------------------

# ================
# ATMOSPHERE MODEL
# ================

def pressure(z):
    """
    Parameters
    ----------
    z : float or np.ndarray
        Altitude [m].

    Returns
    -------
    float or np.ndarray
        Pression atmosphérique [Pa] (loi barométrique).
    """
    P0 = 101325     # Pressure at sea level in Pa
    H = 8500        # Scale height in m
    return P0 * np.exp(-z / H)

def temperature_uniform(z):
    """
    Parameters
    ----------
    z : float or np.ndarray
        Altitude [m] (non utilisée, profil uniforme).

    Returns
    -------
    float or np.ndarray
        Température uniforme 288.2 K sur toute la colonne [K].
    """
    T0 = 288.2
    return T0 * np.ones_like(z)

def temperature_simple(z):
    """
    Parameters
    ----------
    z : float or np.ndarray
        Altitude [m].

    Returns
    -------
    float or np.ndarray
        Température [K] : gradient troposférique linéaire jusqu'à 11 km,
        isotherme au-delà.
    """
    T0 = 288.2     # Temperature at sea level in K
    z_trop = 11000  # Tropopause height in m
    Gamma = -0.0065 # Temperature gradient in K/m
    T_trop = T0 + Gamma * z_trop
    return np.piecewise(z, [z < z_trop, z >= z_trop],
                        [lambda z: T0 + Gamma * z,
                         lambda z: T_trop])

def temperature_US1976(z):
    """
    Parameters
    ----------
    z : float or np.ndarray
        Altitude [m].

    Returns
    -------
    float or np.ndarray
        Température [K] suivant le profil standard US 1976
        (troposphère, tropopause, stratosphère, mésosphère).
    """
    z_km = z/1000  # Convert altitude to km for easier comparisons

    # Troposphere (0 to 11 km)
    T0 = 288.15
    z_trop = 11

    # Tropopause (11 to 20 km)
    T_tropopause = 216.65
    z_tropopause = 20

    # Stratosphere 1 (20 to 32 km)
    T_strat1 = T_tropopause
    z_strat1 = 32

    # Stratosphere 2 (32 to 47 km)
    T_strat2 = 228.65
    z_strat2 = 47

    # Stratopause (47 to 51 km)
    T_stratopause = 270.65
    z_stratopause = 51

    # Mesosphere 1 (51 to 71 km)
    T_meso1 = T_stratopause
    z_meso1 = 71

    # Mesosphere 2 (71 to ...)
    T_meso2 = 214.65

    return np.piecewise(z_km,
                        [z_km < z_trop,
                         (z_km >= z_trop) & (z_km < z_tropopause),
                         (z_km >= z_tropopause) & (z_km < z_strat1),
                         (z_km >= z_strat1) & (z_km < z_strat2),
                         (z_km >= z_strat2) & (z_km < z_stratopause),
                         (z_km >= z_stratopause) & (z_km < z_meso1),
                         z_km >= z_meso1],
                        [lambda z: T0 - 6.5 * z,
                         lambda z: T_tropopause,
                         lambda z: T_strat1 + 1 * (z - z_tropopause),
                         lambda z: T_strat2 + 2.8 * (z - z_strat1),
                         lambda z: T_stratopause,
                         lambda z: T_meso1 - 2.8 * (z - z_stratopause),
                         lambda z: T_meso2 - 2 * (z - z_meso1)])

# ================
# MODELISATIONS GAZ
# ================

# --- Profils verticaux de référence (variation avec l'altitude, 3.2) ---

def concentration_CO2_altitude(altitude_m):
    """
    Parameters
    ----------
    altitude_m : float
        Altitude [m].

    Returns
    -------
    float
        Fraction volumique de CO₂ [-] : 380 ppm jusqu'à 60 km,
        décroissance linéaire jusqu'à 132 km, 0 au-delà.
    """
    if 0 <= altitude_m <= 60000:
        return 380e-6
    elif altitude_m > 132000:
        return 0
    else:
        return (-0.00526 * altitude_m + 736) * 1e-6  # fonction affine

def concentration_O3_altitude(altitude):
    """
    Parameters
    ----------
    altitude : float or np.ndarray
        Altitude [km].

    Returns
    -------
    float or np.ndarray
        Fraction volumique de O₃ [-] : 1 ppm entre 15 et 35 km
        (couche d'ozone stratosphérique), 0 en dehors.
    """
    alt_min = 15  # km
    alt_max = 35  # km

    porte = np.where((altitude >= alt_min) & (altitude <= alt_max), 1.0, 0.0)

    return porte * 1e-6

def concentration_N2O_altitude(altitude_m):
    """
    Parameters
    ----------
    altitude_m : float
        Altitude [m] (non utilisée, valeur constante).

    Returns
    -------
    float
        Fraction volumique de N₂O [-] : 331 ppb constant.
    """
    return 331e-9  # valeur constante pour N₂O

def concentration_CH4_altitude(altitude_m):
    """
    Parameters
    ----------
    altitude_m : float
        Altitude [m].

    Returns
    -------
    float
        Fraction volumique de CH₄ [-] : 1800 ppb en basse troposphère,
        décroissance linéaire entre 9 et 45 km, 100 ppb au-delà.
    """
    if altitude_m < 9000:
        return 1800e-9                                      # valeur à basse altitude
    elif 9000 <= altitude_m <= 45000:
        return (-0.0452 * altitude_m + 2190) * 1e-9
    else:
        return 100e-9

def concentration_H2O_altitude(altitude_m):
    """
    Parameters
    ----------
    altitude_m : float
        Altitude [m] (non utilisée, valeur constante).

    Returns
    -------
    float
        Fraction volumique de H₂O [-] : 400 ppm constant.
    """
    return 400e-6  # valeur constante pour H₂O

# Valeurs de référence au sol utilisées pour la normalisation

_CO2_SOL_REF = 380e-6
_CH4_SOL_REF = 1800e-9
_N2O_SOL_REF = 331e-9
_O3_SOL_REF  = 1e-6 
_H2O_SOL_REF = 400e-6

# --- Concentrations de surface en fonction de l'année (3.1) ---

def concentration_CO2_annee(annee):
    """
    Parameters
    ----------
    annee : int
        Année.

    Returns
    -------
    float
        Concentration de CO₂ au sol [ppm] : 278 ppm avant l'ère industrielle,
        croissance linéaire ensuite.
    """
    if 1838 <= annee <= 1972:
        return 0.294 * annee - 262
    elif annee < 1838:
        return 278
    else:
        return 1.9 * annee - 3430

def concentration_CH4_annee(annee):
    """
    Parameters
    ----------
    annee : int
        Année.

    Returns
    -------
    float
        Concentration de CH₄ au sol [ppm] : croissance linéaire avant 1953,
        plateau à 0.3 ppm ensuite.
    """
    if 1953 <= annee:
        return 300 / 1000
    else:
        return (5.07 * annee - 8.38 * 1000) / 1000

def concentration_N2O_annee(annee):
    """
    Parameters
    ----------
    annee : int
        Année.

    Returns
    -------
    float
        Concentration de N₂O au sol [ppm] : 0.263 ppm avant 1836,
        croissance linéaire ensuite.
    """
    if 1836 <= annee <= 1966:
        return (0.237 * annee - 172) / 1000
    elif annee < 1836:
        return 263 / 1000
    else:
        return (0.77 * annee - 1.22 * 1000) / 1000

def concentration_O3_annee(annee):
    """
    Parameters
    ----------
    annee : int
        Année (non utilisée, valeur constante).

    Returns
    -------
    float
        Concentration totale de O₃ [ppm] : 9 ppm constant.
    """
    return 9  # ppm (constant)

def concentration_H2O_annee(annee):
    """
    Parameters
    ----------
    annee : int
        Année (non utilisée, valeur constante).

    Returns
    -------
    float
        Concentration totale de H₂O [ppm] : 400 ppm constant.
    """
    return 400  # ppm (constant)

# --- Fonctions combinées : profil altitude × facteur annuel ---

def concentration_CO2(z, annee):
    """
    Parameters
    ----------
    z : float
        Altitude [m].
    annee : int
        Année simulée.

    Returns
    -------
    float
        Fraction volumique de CO₂ [-] : profil vertical de référence
        mis à l'échelle par la concentration annuelle au sol.
    """
    facteur = concentration_CO2_annee(annee) * 1e-6 / _CO2_SOL_REF
    return concentration_CO2_altitude(z) * facteur

def concentration_O3(z, annee):
    """
    Parameters
    ----------
    z : float or np.ndarray
        Altitude [km].
    annee : int
        Année simulée.

    Returns
    -------
    float or np.ndarray
        Fraction volumique de O₃ [-] : profil porte mis à l'échelle annuelle.
    """
    facteur = concentration_O3_annee(annee) * 1e-6 / _O3_SOL_REF
    return concentration_O3_altitude(z) * facteur

def concentration_N2O(z, annee):
    """
    Parameters
    ----------
    z : float
        Altitude [m].
    annee : int
        Année simulée.

    Returns
    -------
    float
        Fraction volumique de N₂O [-] : valeur constante mise à l'échelle annuelle.
    """
    facteur = concentration_N2O_annee(annee) * 1e-6 / _N2O_SOL_REF
    return concentration_N2O_altitude(z) * facteur

def concentration_CH4(z, annee):
    """
    Parameters
    ----------
    z : float
        Altitude [m].
    annee : int
        Année simulée.

    Returns
    -------
    float
        Fraction volumique de CH₄ [-] : profil vertical mis à l'échelle annuelle.
    """
    facteur = concentration_CH4_annee(annee) * 1e-6 / _CH4_SOL_REF
    return concentration_CH4_altitude(z) * facteur

def concentration_H2O(z, annee):
    """
    Parameters
    ----------
    z : float
        Altitude [m].
    annee : int
        Année simulée.

    Returns
    -------
    float
        Fraction volumique de H₂O [-] : valeur constante mise à l'échelle annuelle.
    """
    facteur = concentration_H2O_annee(annee) * 1e-6 / _H2O_SOL_REF
    return concentration_H2O_altitude(z) * facteur



# ==> CHOOSE HERE THE TEMPERATURE MODEL
def temperature(z):
    """
    Parameters
    ----------
    z : float or np.ndarray
        Altitude [m].

    Returns
    -------
    float or np.ndarray
        Température atmosphérique [K] selon le profil sélectionné (actuellement US 1976).
    """
    return temperature_US1976(z)

def air_number_density(z):
    """
    Parameters
    ----------
    z : float or np.ndarray
        Altitude [m].

    Returns
    -------
    float or np.ndarray
        Densité numérique de l'air [m⁻³] : n = P / (k_B × T).
    """
    kB = 1.380649e-23  # Boltzmann's constant, J/K
    return pressure(z) / (kB * temperature(z))

# ----------------------------------------------------------------------------------------------------------------------

# ==============
# CO2 ABSORPTION
# ==============

def cross_section_CO2(wavelength):
    """
    Parameters
    ----------
    wavelength : float or np.ndarray
        Longueur d'onde [m].

    Returns
    -------
    float or np.ndarray
        Section efficace d'absorption du CO₂ [m²] centrée à 15 µm.
    """
    LAMBDA_0 = 15.0e-6  # Band center in m
    exponent = -24.1 - 20.9 * np.abs((wavelength - LAMBDA_0) / LAMBDA_0)
    #exponent = -22.5 - 24 * np.abs((wavelength - LAMBDA_0) / LAMBDA_0)
    sigma = 10 ** exponent
    return sigma

def cross_section_O3(wavelength):
    """
    Parameters
    ----------
    wavelength : float or np.ndarray
        Longueur d'onde [m].

    Returns
    -------
    float or np.ndarray
        Section efficace d'absorption du O₃ [m²] centrée à 9.4 µm.
    """
    LAMBDA_0 = 9.4e-6
    exponent = -23 - 15 * np.abs((wavelength - LAMBDA_0) / LAMBDA_0) 
    #exponent = -22.6 - 32.2 * np.abs((wavelength - LAMBDA_0) / LAMBDA_0)
    return 10 ** exponent

def cross_section_N2O(wavelength):
    """
    Parameters
    ----------
    wavelength : float or np.ndarray
        Longueur d'onde [m].

    Returns
    -------
    float or np.ndarray
        Section efficace d'absorption du N₂O [m²] centrée à 17 µm.
    """
    LAMBDA_0 = 17e-6 
    exponent = -23.9 - 24.8 * np.abs((wavelength - LAMBDA_0) / LAMBDA_0)    #25e-6           #16.4
    #exponent = -23.2 - 26.3 * np.abs((wavelength - LAMBDA_0) / LAMBDA_0)
    return 10 ** exponent

def cross_section_CH4(wavelength):
    """
    Parameters
    ----------
    wavelength : float or np.ndarray
        Longueur d'onde [m].

    Returns
    -------
    float or np.ndarray
        Section efficace d'absorption du CH₄ [m²] : somme de deux bandes
        centrées à 7.65 µm et 3.35 µm.
    """
    LAMBDA_1 = 7.65e-6 #7.65e-6
    LAMBDA_2 = 3.35e-6#3.35e-6
    exponent1 = - 24 - 16.4 * np.abs((wavelength - LAMBDA_1) / LAMBDA_1)
    exponent2 = - 25 - 8.5 * np.abs((wavelength - LAMBDA_2) / LAMBDA_2)
    #exponent1 = -23.10 - 17.55 * np.abs((wavelength - LAMBDA_1) / LAMBDA_1)
    #exponent2 = -23.20 - 14.64 * np.abs((wavelength - LAMBDA_2) / LAMBDA_2)
    return 10 ** exponent1 + 10 ** exponent2

#def cross_section_H20(wavelength):
    LAMBDA_REF = 7.65e-6
    LAMBDA_0 = 5e-6
    A = -23.0
    n = -1.01
    B = -23.5
    C = 8.0
    exponent = B - C * np.abs((wavelength - LAMBDA_0)/LAMBDA_0)
    return 10**exponent + 10**A * (wavelength / LAMBDA_REF)**n
    

#def cross_section_H2O(wavelength):
    # Continuum H2O : croissance type loi de puissance vers les grandes longueurs d'onde
    # (rotation pure), avec un plancher dans l'IR moyen
    #LAMBDA_REF = 50e-6
    #A = -23.0
    #n = 10.0  # exposant de croissance
    #return 10**A * (wavelength / LAMBDA_REF)**n
    
def cross_section_H2O(wavelength):
    """
    Parameters
    ----------
    wavelength : float or np.ndarray
        Longueur d'onde [m].

    Returns
    -------
    float or np.ndarray
        Section efficace d'absorption du H₂O [m²] centrée à 6.3 µm.
    """
    LAMBDA_0 = 6.3e-6
    A = -23.3
    B = 14
    return 10**(A - B * np.abs((wavelength - LAMBDA_0)/LAMBDA_0))

# =============================
# RADIATIVE TRANSFER SIMULATION
# =============================

# All wavelengths are treated in parallel using vectorization

def simulate_radiative_transfer(annee, z_max = 80000, delta_z = 10, lambda_min = 0.1e-6, lambda_max = 100e-6, delta_lambda = 0.01e-6):
    """
    Parameters
    ----------
    annee : int
        Année simulée (détermine les concentrations des gaz à effet de serre).
    z_max : float, optional
        Altitude maximale de la colonne [m]. The default is 80000.
    delta_z : float, optional
        Pas vertical [m]. The default is 10.
    lambda_min : float, optional
        Longueur d'onde minimale [m]. The default is 0.1e-6.
    lambda_max : float, optional
        Longueur d'onde maximale [m]. The default is 100e-6.
    delta_lambda : float, optional
        Pas spectral [m]. The default is 0.01e-6.

    Returns
    -------
    lambda_range : np.ndarray
        Grille de longueurs d'onde [m].
    z_range : np.ndarray
        Grille d'altitudes [m].
    upward_flux : np.ndarray
        Flux montant à chaque couche et longueur d'onde [W m⁻²],
        de forme (len(z_range), len(lambda_range)).
    optical_thickness : np.ndarray
        Épaisseur optique de chaque couche [-], même forme.
    mean_flux_top : float
        Flux total sortant au sommet de l'atmosphère [W m⁻²].
    """

    # Altitude and wavelength grids
    z_range = np.arange(0, z_max, delta_z)
    lambda_range = np.arange(lambda_min, lambda_max, delta_lambda)

    # Initialize arrays
    upward_flux = np.zeros((len(z_range), len(lambda_range)))
    optical_thickness = np.zeros((len(z_range), len(lambda_range)))

    # Boundary condition : Compute the outward vertical flux emitted by the Earth's surface for all wavelengths
    earth_flux = np.pi * planck_function(lambda_range, temperature(0)) * delta_lambda
    print(f"Total earth surface flux in wavelength range: {earth_flux.sum():.2f} W/m^2")

    flux_in = earth_flux
    n_total = len(z_range)
    for i, z in enumerate(z_range):

        if i % (n_total // 20) == 0:
            pct = int(100 * i / n_total)
            barre = '█' * (pct // 5) + '░' * (20 - pct // 5)
            print(f"\r  Transfert radiatif : [{barre}] {pct:3d}%  z = {z/1000:.1f} km", end='', flush=True)

        # Concentrations combinant profil d'altitude (3.2) et facteur annuel (3.1)
        n_CO2 = air_number_density(z) * concentration_CO2(z, annee)
        n_O3  = air_number_density(z) * concentration_O3(z, annee)
        n_N2O = air_number_density(z) * concentration_N2O(z, annee)
        n_CH4 = air_number_density(z) * concentration_CH4(z, annee)
        n_H20 = air_number_density(z) * concentration_H2O(z, annee)

        kappa = cross_section_CO2(lambda_range) * n_CO2 + cross_section_N2O(lambda_range) * n_N2O + cross_section_O3(lambda_range) * n_O3 + cross_section_CH4(lambda_range) * n_CH4 #+ cross_section_H2O(lambda_range) * n_H20

        # Compute fluxes within the layer
        optical_thickness[i,:] = kappa * delta_z
        absorbed_flux = np.minimum(kappa * delta_z * flux_in , flux_in)
        emitted_flux = optical_thickness[i,:] * np.pi * planck_function(lambda_range, temperature(z)) * delta_lambda 
        upward_flux[i, :] = flux_in - absorbed_flux + emitted_flux

        # The flux leaving the layer becomes the flux entering the next layer
        flux_in = upward_flux[i, :]

    print(f"\r  Transfert radiatif : [{'█'*20}] 100%  z = {z_max/1000:.1f} km")
    mean_flux_top = upward_flux[-1, :].sum()
    print(f"Total outgoing flux at the top of the atmosphere: {mean_flux_top:.2f} W/m^2")

    return lambda_range, z_range, upward_flux, optical_thickness, mean_flux_top

# ----------------------------------------------------------------------------------------------------------------------