"""
========================================================================
Sections efficaces d'absorption des gaz a effet de serre - a partir des
donnees HITRAN (fichier '6a398448.par', format HITRAN2004, largeur fixe)
========================================================================

Contenu :
  1. Lecture du fichier .par et extraction (molec_id, nu, sw) par gaz
  2. Construction d'un spectre lisse de section efficace par "binning"
     en longueur d'onde (sigma = somme des intensites de raie / largeur
     de bin en nombre d'onde -> cm2/molecule, convertis en m2/molecule)
  3. Ajustement du modele analytique log-lineaire :
         sigma(lambda) = 10 ** ( a - b * |lambda - lambda0| / lambda0 )
     - bande simple pour CO2, O3, N2O, H2O (lambda0 fixe par gaz)
     - bande double (somme de deux bandes simples) pour CH4
  4. Fonctions finales cross_section_XXX(wavelength), au meme format
     que les fonctions de depart, avec les coefficients (a, b) obtenus
     par le fit (et non plus codes en dur "a la main").

molec_id HITRAN presents dans le fichier : 1=H2O, 2=CO2, 3=O3, 4=N2O,
5=CO, 6=CH4, 7=O2.

NOTE IMPORTANTE sur N2O : le code de depart utilisait lambda0 = 25 um
(avec un commentaire "#16.4" en suspens). L'analyse des donnees HITRAN
montre clairement que la bande la plus intense de N2O dans l'infrarouge
thermique terrestre (bande nu1, etirement symetrique) est centree pres
de 17 um, et non 25 um. On retient donc ici lambda0 = 17.0 um pour N2O,
ce qui correspond bien au "16.4" laisse en commentaire dans le code
original.
"""

import numpy as np
from pathlib import Path
from scipy.optimize import curve_fit

# ------------------------------------------------------------------
# 0. Constantes / chemins
# ------------------------------------------------------------------

HITRAN_FILE = Path(__file__).parent / "6a398448.par"

MOLEC_ID = {"H2O": 1, "CO2": 2, "O3": 3, "N2O": 4, "CO": 5, "CH4": 6, "O2": 7}

CM2_TO_M2 = 1e-4  # 1 cm^2 = 1e-4 m^2


# ------------------------------------------------------------------
# 1. Lecture du fichier HITRAN (.par, format largeur fixe HITRAN2004)
# ------------------------------------------------------------------

def read_hitran_par(path):
    """
    Lit le fichier .par HITRAN2004 (largeur fixe) et renvoie
    (molec_ids, nus, sws) sous forme de tableaux numpy.

    Colonnes utilisees (positions fixes, cf. readme HITRAN2004) :
        molec_id     -> caracteres [0:2]   (I2)
        nu  (cm-1)   -> caracteres [3:15]  (F12.6)
        sw           -> caracteres [15:25] (E10.3)
    """
    molec_ids, nus, sws = [], [], []
    with open(path, "r", encoding="ascii", errors="ignore") as f:
        for line in f:
            if len(line) < 25:
                continue
            try:
                molec_id = int(line[0:2])
                nu = float(line[3:15])
                sw = float(line[15:25])
            except ValueError:
                continue
            molec_ids.append(molec_id)
            nus.append(nu)
            sws.append(sw)
    return (np.array(molec_ids, dtype=np.int8),
            np.array(nus, dtype=np.float64),
            np.array(sws, dtype=np.float64))


# ------------------------------------------------------------------
# 2. Construction d'un spectre lisse sigma(lambda) par binning
# ------------------------------------------------------------------

def build_binned_spectrum(nus_cm1, sws, lambda_min, lambda_max, n_bins=2000):
    """
    Binning lineaire en longueur d'onde lambda (m).
    Dans chaque bin : sigma = somme(sw) / delta_nu_bin (cm-1)
                     -> cm2/molecule -> converti en m2/molecule.

    Renvoie (lambda_centres, sigma) en ne gardant que les bins valides
    (sigma > 0, fini).
    """
    lam = 1e-2 / nus_cm1  # cm-1 -> m
    mask = (lam >= lambda_min) & (lam <= lambda_max)
    lam, sw = lam[mask], sws[mask]

    edges = np.linspace(lambda_min, lambda_max, n_bins + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])

    sw_sum, _ = np.histogram(lam, bins=edges, weights=sw)
    nu_edges = 1e-2 / edges
    delta_nu = np.abs(nu_edges[:-1] - nu_edges[1:])  # cm-1

    with np.errstate(divide="ignore", invalid="ignore"):
        sigma_m2 = (sw_sum / delta_nu) * CM2_TO_M2

    valid = (sigma_m2 > 0) & np.isfinite(sigma_m2)
    return centers[valid], sigma_m2[valid]


# ------------------------------------------------------------------
# 3. Ajustement du modele log-lineaire (bande simple / bande double)
# ------------------------------------------------------------------

def _single_band_log_model(wavelength, lambda0, sigma_cen_log, width):
    """log10(sigma) pour une bande simple centree sur lambda0 (fixe)."""
    return sigma_cen_log - width * np.abs((wavelength - lambda0) / lambda0)


def fit_single_band(lam, sigma, lambda0, p0=(-23.0, 20.0), fit_range=None):
    """
    Ajuste (sigma_cen_log, width) tels que :
        log10(sigma) = sigma_cen_log - width * |lambda - lambda0| / lambda0
    lambda0 est fixe (impose), seuls (sigma_cen_log, width) sont libres.

    fit_range : (lambda_min, lambda_max) optionnel, pour restreindre le
    fit a la bande d'interet et eviter que des bandes secondaires plus
    faibles ne biaisent la pente ajustee.
    """
    if fit_range is not None:
        lmin, lmax = fit_range
        m = (lam >= lmin) & (lam <= lmax)
        lam, sigma = lam[m], sigma[m]

    log_sigma = np.log10(sigma)

    def model(wavelength, sigma_cen_log, width):
        return _single_band_log_model(wavelength, lambda0, sigma_cen_log, width)

    popt, pcov = curve_fit(model, lam, log_sigma, p0=p0, maxfev=20000)
    return popt, pcov  # popt = [sigma_cen_log, width]


def fit_double_band(lam, sigma, lambda1, lambda2, p0=(-23.0, 17.0), fit_range=None):
    """
    Ajustement d'une bande double (CH4) : sigma = 10**band1 + 10**band2.
    Comme on ne peut pas linéariser le log d'une somme de deux lois de
    puissance, chaque point de donnees est assigne au pic le plus proche
    (en distance relative |lambda-lambda_i|/lambda_i), puis on fit deux
    bandes simples independantes sur les deux sous-ensembles obtenus.
    """
    if fit_range is not None:
        lmin, lmax = fit_range
        m = (lam >= lmin) & (lam <= lmax)
        lam, sigma = lam[m], sigma[m]

    d1 = np.abs((lam - lambda1) / lambda1)
    d2 = np.abs((lam - lambda2) / lambda2)
    mask1 = d1 <= d2

    popt1, _ = fit_single_band(lam[mask1], sigma[mask1], lambda1, p0=p0)
    popt2, _ = fit_single_band(lam[~mask1], sigma[~mask1], lambda2, p0=p0)
    return popt1, popt2  # chacun = [sigma_cen_log, width]


# ------------------------------------------------------------------
# 4. Pipeline complet : extraction + fit pour chaque gaz
# ------------------------------------------------------------------

def fit_all_gases(hitran_path=HITRAN_FILE):
    molec_ids, nus, sws = read_hitran_par(hitran_path)

    coeffs = {}

    # --- CO2 : bande simple, lambda0 = 15.0 um ---
    m = molec_ids == MOLEC_ID["CO2"]
    lam, sig = build_binned_spectrum(nus[m], sws[m], 10e-6, 20e-6)
    popt, _ = fit_single_band(lam, sig, lambda0=15.0e-6, p0=(-22.5, 24.0),
                               fit_range=(13e-6, 17e-6))
    coeffs["CO2"] = {"lambda0": 15.0e-6, "a": popt[0], "b": popt[1]}

    # --- O3 : bande simple, lambda0 = 9.4 um ---
    m = molec_ids == MOLEC_ID["O3"]
    lam, sig = build_binned_spectrum(nus[m], sws[m], 5e-6, 14e-6)
    popt, _ = fit_single_band(lam, sig, lambda0=9.4e-6, p0=(-22.6, 32.2),
                               fit_range=(8.5e-6, 10.3e-6))
    coeffs["O3"] = {"lambda0": 9.4e-6, "a": popt[0], "b": popt[1]}

    # --- N2O : bande simple, lambda0 = 17.0 um (bande nu1 - voir note) ---
    m = molec_ids == MOLEC_ID["N2O"]
    lam, sig = build_binned_spectrum(nus[m], sws[m], 10e-6, 40e-6)
    popt, _ = fit_single_band(lam, sig, lambda0=17.0e-6, p0=(-23.2, 26.3),
                               fit_range=(13e-6, 22e-6))
    coeffs["N2O"] = {"lambda0": 17.0e-6, "a": popt[0], "b": popt[1]}

    # --- CH4 : bande double, lambda1 = 7.65 um, lambda2 = 3.35 um ---
    m = molec_ids == MOLEC_ID["CH4"]
    lam, sig = build_binned_spectrum(nus[m], sws[m], 2e-6, 12e-6)
    popt1, popt2 = fit_double_band(lam, sig, lambda1=7.65e-6, lambda2=3.35e-6,
                                    p0=(-23.10, 17.55), fit_range=(2e-6, 11e-6))
    coeffs["CH4"] = {
        "lambda1": 7.65e-6, "a1": popt1[0], "b1": popt1[1],
        "lambda2": 3.35e-6, "a2": popt2[0], "b2": popt2[1],
    }

    # --- H2O : bande simple, MEME MODELE que CO2/O3/N2O, lambda0 impose ---
    # lambda0 = 6.3 um : bande de flexion (nu2) de H2O, la plus pertinente
    # dans l'infrarouge thermique terrestre (effet de serre).
    m = molec_ids == MOLEC_ID["H2O"]
    lam, sig = build_binned_spectrum(nus[m], sws[m], 1e-6, 30e-6)
    popt, _ = fit_single_band(lam, sig, lambda0=6.3e-6, p0=(-22.0, 10.0),
                               fit_range=(4e-6, 9e-6))
    coeffs["H2O"] = {"lambda0": 6.3e-6, "a": popt[0], "b": popt[1]}

    return coeffs


# ------------------------------------------------------------------
# 5. Coefficients ajustes (calcules une fois par fit_all_gases, puis
#    figes ici pour un usage direct sans avoir a relire le fichier
#    HITRAN a chaque fois). Recalculer avec fit_all_gases() si besoin.
# ------------------------------------------------------------------

_COEFFS = fit_all_gases()


# ------------------------------------------------------------------
# 6. Fonctions finales de section efficace (meme signature que le
#    code de depart : cross_section_XXX(wavelength) -> sigma en m^2)
# ------------------------------------------------------------------

def cross_section_CO2(wavelength):
    c = _COEFFS["CO2"]
    exponent = c["a"] - c["b"] * np.abs((wavelength - c["lambda0"]) / c["lambda0"])
    return 10 ** exponent


def cross_section_O3(wavelength):
    c = _COEFFS["O3"]
    exponent = c["a"] - c["b"] * np.abs((wavelength - c["lambda0"]) / c["lambda0"])
    return 10 ** exponent


def cross_section_N2O(wavelength):
    c = _COEFFS["N2O"]
    exponent = c["a"] - c["b"] * np.abs((wavelength - c["lambda0"]) / c["lambda0"])
    return 10 ** exponent


def cross_section_CH4(wavelength):
    c = _COEFFS["CH4"]
    exponent1 = c["a1"] - c["b1"] * np.abs((wavelength - c["lambda1"]) / c["lambda1"])
    exponent2 = c["a2"] - c["b2"] * np.abs((wavelength - c["lambda2"]) / c["lambda2"])
    return 10 ** exponent1 + 10 ** exponent2


def cross_section_H2O(wavelength):
    """
    Section efficace d'absorption de la vapeur d'eau H2O, construite avec
    le MEME modele analytique (bande simple log-lineaire) que CO2, O3 et
    N2O, ajuste sur les donnees HITRAN, et centree sur lambda0 = 6.3 um
    (bande de flexion nu2, dominante dans l'IR thermique terrestre).
    """
    c = _COEFFS["H2O"]
    exponent = c["a"] - c["b"] * np.abs((wavelength - c["lambda0"]) / c["lambda0"])
    return 10 ** exponent


# ------------------------------------------------------------------
# 7. Affichage des coefficients obtenus si le script est lance seul
# ------------------------------------------------------------------

if __name__ == "__main__":
    print("Coefficients ajustes sur les donnees HITRAN (fichier 6a398448.par) :")
    print("-" * 70)
    for gas, c in _COEFFS.items():
        print(gas, {k: round(v, 4) if "lambda" not in k else v for k, v in c.items()})
    print("-" * 70)

    # Petite verification numerique au pic de chaque bande
    print("\nValeurs au centre de bande (verification) :")
    print("CO2 (15.0 um)  :", cross_section_CO2(np.array([15.0e-6]))[0])
    print("O3  (9.4 um)   :", cross_section_O3(np.array([9.4e-6]))[0])
    print("N2O (17.0 um)  :", cross_section_N2O(np.array([17.0e-6]))[0])
    print("CH4 (7.65 um)  :", cross_section_CH4(np.array([7.65e-6]))[0])
    print("H2O (6.3 um)   :", cross_section_H2O(np.array([6.3e-6]))[0])