# -*- coding: utf-8 -*-
"""
transfert_radiatif.py — Modèle 2.2.

Simule le transfert radiatif spectral couche par couche dans la colonne
atmosphérique (≈8 000 couches de 10 m de 0 à 80 km).

Gaz pris en compte : CO₂, CH₄, N₂O, O₃, H₂O (H₂O désactivé en pratique).
Différence vs Modèle 2.1 : les concentrations varient avec l'altitude
(profils verticaux réalistes). L'année est fixée à 2026 (pas de paramètre temporel).

Physique implémentée :
  - Loi de Planck : B_λ(T) = 2hc²/λ⁵ / (exp(hc/λkT) - 1)
  - Loi barométrique : P(z) = P₀ × exp(-z/H), H = 8500 m
  - Profil de température atmosphérique standard US 1976
  - Sections efficaces d'absorption gaussiennes (ajustées par régression)
  - Transfert Beer-Lambert : flux_sorti = flux_in - absorbé + émis
"""
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------

# ===================
# BLACKBODY RADIATION
# ===================

def planck_function(lambda_wavelength, T):
    """
    Luminance spectrale d'un corps noir [W m⁻² sr⁻¹ m⁻¹] à la température T.
    Formule : B_λ = (2hc²/λ⁵) / (exp(hc/λkT) - 1)
    """
    h = 6.62607015e-34      # Constante de Planck [J·s]
    c = 2.998e8             # Vitesse de la lumière dans le vide [m/s]
    kB = 1.380649e-23       # Constante de Boltzmann [J/K]
    term1 = (2 * h * c**2) / lambda_wavelength**5   # Numérateur de la loi de Planck
    term2 = np.exp((h * c) / (lambda_wavelength * kB * T)) - 1  # Dénominateur (facteur de Bose-Einstein)
    return term1 / term2

# ----------------------------------------------------------------------------------------------------------------------

# ================
# ATMOSPHERE MODEL
# ================

def pressure(z):
    """Pression atmosphérique [Pa] selon la loi barométrique : P(z) = P₀ × exp(-z/H)."""
    P0 = 101325     # Pression au niveau de la mer [Pa]
    H = 8500        # Hauteur d'échelle [m] (distance caractéristique de décroissance)
    return P0 * np.exp(-z / H)

def temperature_uniform(z):
    """Profil de température uniforme (modèle simplifié, T = constante)."""
    T0 = 288.2
    return T0 * np.ones_like(z)

def temperature_simple(z):
    """Gradient linéaire jusqu'à la tropopause, puis isotherme au-delà."""
    T0 = 288.2      # Température au niveau de la mer [K]
    z_trop = 11000  # Hauteur de la tropopause [m]
    Gamma = -0.0065 # Gradient thermique [K/m] (refroidissement avec l'altitude)
    T_trop = T0 + Gamma * z_trop
    return np.piecewise(z, [z < z_trop, z >= z_trop],
                        [lambda z: T0 + Gamma * z,
                         lambda z: T_trop])

def temperature_US1976(z):
    """Profil de température par couches suivant l'Atmosphère Standard Américaine 1976."""
    z_km = z / 1000  # Conversion altitude m → km

    # Troposphere (0 à 11 km) : refroidissement linéaire
    T0 = 288.15
    z_trop = 11
    # Tropopause (11 à 20 km) : isotherme
    T_tropopause = 216.65
    z_tropopause = 20
    # Stratosphère 1 (20 à 32 km) : réchauffement (absorption UV par l'ozone)
    T_strat1 = T_tropopause
    z_strat1 = 32
    # Stratosphère 2 (32 à 47 km) : continuation du réchauffement
    T_strat2 = 228.65
    z_strat2 = 47
    # Stratopause (47 à 51 km) : maximum de température stratosphérique
    T_stratopause = 270.65
    z_stratopause = 51
    # Mésosphère 1 (51 à 71 km) : refroidissement
    T_meso1 = T_stratopause
    z_meso1 = 71
    # Mésosphère 2 (au-delà de 71 km) : continuation du refroidissement
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
def concentration_CO2_altitude(altitude_m):
    """
    Renvoie la fraction volumique de CO₂ (sans dimension) pour une altitude en mètres.
    """
    if 0 <= altitude_m <= 60000:
        return 380e-6
    elif altitude_m > 132000:
        return 0
    else:
        return (-0.00526 * altitude_m + 736) * 1e-6  # fonction affine


def concentration_O3_altitude(altitude):
    """
    Modélise la concentration d'ozone (en ppm) par une fonction porte
    selon l'altitude (en km) pour une année donnée.
    """
    alt_min = 15000 # km
    alt_max = 35000  # km
    
    if alt_min <= altitude <= alt_max:
        return 8.5*10**(-6)
    else : return 0
    
    
 

def concentration_N2O_altitude(altitude):
    """
    Renvoie la proportion estimée de N₂O en ppm pour une altitude donnée.
    """
    return 331e-9  # valeur constante pour N₂O

def concentration_CH4_altitude(altitude_m):
    """
    Renvoie la fraction volumique de CH₄ (sans dimension) pour une altitude en mètres.
    """
    if altitude_m < 9000:
        return 1800e-9                                      # valeur à basse altitude
    elif 9000 <= altitude_m <= 45000:
        return (-0.0452 * altitude_m + 2190) * 1e-9        # fonction affine
    else:
        return 100e-9                                       # valeur à haute altitude

def concentration_H2O_altitude(altitude):
    """
    Renvoie la proportion estimée de H₂O en ppm pour une altitude donnée.
    """
    return 400e-6  # valeur constante pour H₂O



# ==> CHOOSE HERE THE TEMPERATURE MODEL
def temperature(z):
    return temperature_US1976(z)

def air_number_density(z):
    kB = 1.380649e-23  # Boltzmann's constant, J/K
    return pressure(z) / (kB * temperature(z))

# ----------------------------------------------------------------------------------------------------------------------

# ==============
# CO2 ABSORPTION
# ==============

def cross_section_CO2(wavelength):
    LAMBDA_0 = 15.0e-6  # Band center in m
    exponent = -24.1 - 20.9 * np.abs((wavelength - LAMBDA_0) / LAMBDA_0)
    #exponent = -22.5 - 24 * np.abs((wavelength - LAMBDA_0) / LAMBDA_0)
    sigma = 10 ** exponent
    return sigma

def cross_section_O3(wavelength):
    LAMBDA_0 = 9.4e-6
    exponent = -23 - 15 * np.abs((wavelength - LAMBDA_0) / LAMBDA_0) 
    #exponent = -22.6 - 32.2 * np.abs((wavelength - LAMBDA_0) / LAMBDA_0)
    return 10 ** exponent

def cross_section_N2O(wavelength):
    LAMBDA_0 = 17e-6 
    exponent = -23.9 - 24.8 * np.abs((wavelength - LAMBDA_0) / LAMBDA_0)    #25e-6           #16.4
    #exponent = -23.2 - 26.3 * np.abs((wavelength - LAMBDA_0) / LAMBDA_0)
    return 10 ** exponent

def cross_section_CH4(wavelength):
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
    LAMBDA_0 = 6.3e-6
    A = -23.3
    B = 14
    return 10**(A - B * np.abs((wavelength - LAMBDA_0)/LAMBDA_0))

# =============================
# RADIATIVE TRANSFER SIMULATION
# =============================

# All wavelengths are treated in parallel using vectorization

def simulate_radiative_transfer(z_max = 80000, delta_z = 10, lambda_min = 0.1e-6, lambda_max = 100e-6, delta_lambda = 0.01e-6):

    # Grilles d'altitude [m] et de longueur d'onde [m] discrétisées
    z_range = np.arange(0, z_max, delta_z)
    lambda_range = np.arange(lambda_min, lambda_max, delta_lambda)

    # Initialisation des matrices résultat
    upward_flux = np.zeros((len(z_range), len(lambda_range)))       # Flux montant par couche et longueur d'onde [W m⁻²]
    optical_thickness = np.zeros((len(z_range), len(lambda_range))) # Épaisseur optique par couche [-]

    # Condition aux limites : flux émis par la surface terrestre (corps noir à T=288 K)
    # π × B_λ(T) × Δλ donne le flux hémisphérique [W m⁻²] pour chaque intervalle spectral
    earth_flux = np.pi * planck_function(lambda_range, temperature(0)) * delta_lambda
    print(f"Flux de surface terrestre dans l'intervalle spectral : {earth_flux.sum():.2f} W/m²")

    flux_in = earth_flux  # Flux entrant dans la première couche = flux de surface
    for i, z in enumerate(z_range):

        # --- Densités moléculaires de chaque GES [m⁻³] à l'altitude z ---
        # Les concentrations varient avec l'altitude (profils réalistes)
        n_CO2 = air_number_density(z) * concentration_CO2_altitude(z)
        n_O3  = air_number_density(z) * concentration_O3_altitude(z)
        n_N2O = air_number_density(z) * concentration_N2O_altitude(z)
        n_CH4 = air_number_density(z) * concentration_CH4_altitude(z)
        n_H20 = air_number_density(z) * concentration_H2O_altitude(z)

        # --- Coefficient d'extinction total kappa [m⁻¹] ---
        # kappa_λ = Σ (σ_λ,GES × n_GES) où σ [m²/molécule] est la section efficace d'absorption
        # H₂O est désactivé : le modèle gaussien utilisé est insuffisamment précis
        kappa = (cross_section_CO2(lambda_range) * n_CO2 + cross_section_N2O(lambda_range) * n_N2O
                 + cross_section_O3(lambda_range) * n_O3 + cross_section_CH4(lambda_range) * n_CH4)
                 # + cross_section_H20(lambda_range) * n_H20  # désactivé

        # --- Loi de Beer-Lambert : propagation dans la couche d'épaisseur delta_z ---
        # Épaisseur optique τ = kappa × δz (adimensionnel) : mesure l'opacité de la couche
        optical_thickness[i, :] = kappa * delta_z

        # Flux absorbé par la couche : approximation linéaire de (1 - e^{-τ}) ≈ τ pour τ << 1
        # np.minimum évite d'absorber plus que le flux disponible
        absorbed_flux = np.minimum(kappa * delta_z * flux_in, flux_in)

        # Flux réémis thermiquement par la couche (corps gris, émissivité ε = τ)
        # Le facteur π convertit la luminance [W m⁻² sr⁻¹ m⁻¹] en flux hémisphérique [W m⁻² m⁻¹]
        emitted_flux = optical_thickness[i, :] * np.pi * planck_function(lambda_range, temperature(z)) * delta_lambda

        # Flux montant sortant de la couche : flux incident − absorbé + réémis
        upward_flux[i, :] = flux_in - absorbed_flux + emitted_flux

        # Ce flux sortant devient le flux incident de la couche suivante
        flux_in = upward_flux[i, :]

    mean_flux_top = upward_flux[-1, :].sum()  # Flux total sortant au sommet de l'atmosphère [W m⁻²]
    print(f"Flux sortant au sommet de l'atmosphère : {mean_flux_top:.2f} W/m²")

    return lambda_range, z_range, upward_flux, optical_thickness, mean_flux_top

# ----------------------------------------------------------------------------------------------------------------------

# MAIN


# N2O_fraction = 331e-9 #(en ppm)
# O3_fraction = 6e-6
# CH4_fraction = 2000e-9
# H20_fraction = 400e-6
# lambda_range, z_range, upward_flux, optical_thickness, mean_flux_top = simulate_radiative_transfer(O3_fraction, N2O_fraction, CH4_fraction, H20_fraction)
# CO2_fraction *= 2
# N2O_fraction *= 1
# O3_fraction *= 1
# CH4_fraction *= 1
# H20_fraction *= 1
# lambda_range, z_range, upward_flux2, optical_thickness2, mean_flux_top2  = simulate_radiative_transfer(O3_fraction, N2O_fraction, CH4_fraction, H20_fraction)

# # Plot top of atmosphere spectrum
# plt.figure(figsize=(14, 9))
# # Superimpose blackbody spectrum at Earth's surface temperature and 220K
# plt.plot(1e6 * lambda_range, np.pi * planck_function(lambda_range, temperature(0))/1e6,'--k')
# plt.plot(1e6 * lambda_range, np.pi * planck_function(lambda_range, 216)/1e6,'--k')

# delta_lambda = lambda_range[1] - lambda_range[0]
# plt.plot(1e6 * lambda_range, upward_flux[-1, :]/delta_lambda/1e6,'-g')
# plt.plot(1e6 * lambda_range, upward_flux2[-1, :]/delta_lambda/1e6,'-r')
# plt.fill_between(1e6 * lambda_range, upward_flux[-1, :]/delta_lambda/1e6, upward_flux2[-1, :]/delta_lambda/1e6, color='yellow', alpha=0.9)
# plt.xlabel("Longueur d'onde (μm)")
# plt.ylabel("Luminance spectrale (W/m²/μm/sr)")
# plt.xlim(0, 50)
# plt.ylim(0, 30)
# plt.grid(True)
# plt.show()
# # ----------------------------------------------------------------------------------------------------------------------