# -*- coding: utf-8 -*-
"""
fonction_calcul_alpha.py — Modèle 2.1.

Calcule le coefficient alpha en prenant en compte 5 gaz à effet de serre
(CO₂, CH₄, N₂O, O₃, H₂O) dont les concentrations de surface dépendent
de l'année simulée. Les profils verticaux sont uniformes (concentration
constante sur toute la colonne atmosphérique).

Interprétation physique d'alpha :
  - alpha = flux sortant sommet atmosphère / flux émis par la surface
  - (1 - alpha) = fraction réabsorbée et renvoyée vers la surface (effet de serre)
"""
from . import transfert_radiatif as c_a


# ────────────────────────────────────────────────────────────
# CONCENTRATIONS DE SURFACE PAR GES EN FONCTION DE L'ANNÉE
# ────────────────────────────────────────────────────────────

def concentration_CO2(annee):
    """
    Concentration de CO₂ en surface [ppm] pour l'année donnée.
    Modèle empirique par morceaux (pré-industriel, croissance lente, croissance rapide).
    """
    if 1838 <= annee <= 1972:
        return 0.294 * annee - 262
    elif annee < 1838:
        return 278        # Valeur pré-industrielle [ppm]
    else:
        return 1.9 * annee - 3430


def concentration_CH4(annee):
    """
    Concentration de CH₄ en surface [ppm] pour l'année donnée.
    Seuil à 675 ppb (0.675 ppm) à partir de 1786 (début de l'industrialisation).
    """
    if 1786 <= annee:
        return 675 / 1000    # Valeur post-1786 [ppm]
    else:
        return (5.07 * annee - 8.38 * 1000) / 1000


def concentration_N2O(annee):
    """
    Concentration de N₂O en surface [ppm] pour l'année donnée.
    """
    if 1836 <= annee <= 1966:
        return (0.237 * annee - 172) / 1000
    elif annee < 1836:
        return 263 / 1000   # Valeur pré-industrielle [ppm]
    else:
        return (0.77 * annee - 1.22 * 1000) / 1000


def concentration_03(annee):
    """Concentration d'O₃ [ppm] — valeur fixe (simplification Modèle 2.1)."""
    return 9  # ppm (constante, non calibrée sur l'année dans ce modèle)


def concentration_H2O(annee):
    """Concentration de H₂O [ppm] — valeur fixe (simplification Modèle 2.1)."""
    return 400  # ppm (valeur typique tropique basse altitude)


# ────────────────────────────────────────────────────────────
# CALCUL D'ALPHA
# ────────────────────────────────────────────────────────────

def calcul_alpha(P_emis, annee):
    """
    Calcule alpha : fraction du flux IR de surface s'échappant vers l'espace.

    Parameters
    ----------
    P_emis : float
        Flux thermique émis par la surface [W m⁻²].
    annee : int
        Année simulée (concentrations de surface des 5 GES).

    Returns
    -------
    float
        alpha [-] : fraction du flux de surface qui traverse l'atmosphère.
    """
    # Conversion des concentrations annuelles de ppm → fractions volumiques [-]
    taux_CO2 = concentration_CO2(annee) * 1e-6
    taux_CH4 = concentration_CH4(annee) * 1e-6
    taux_N2O = concentration_N2O(annee) * 1e-6
    taux_O3  = concentration_03(annee)  * 1e-6
    taux_H2O = concentration_H2O(annee) * 1e-6

    # Simulation du transfert radiatif avec les 5 GES (concentrations uniformes en altitude)
    lambda_rxange, z_range, upward_flux, optical_thickness, earth_flux = (
        c_a.simulate_radiative_transfer(taux_CO2, taux_CH4, taux_N2O, taux_O3, taux_H2O)
    )

    # Flux total sortant au sommet de l'atmosphère [W m⁻²]
    mean_flux_top = upward_flux[-1, :].sum()

    flux_emis_terre = P_emis  # Flux émis par la surface [W m⁻²]

    # alpha = flux sortant / flux de surface
    # (1-alpha) est réabsorbé par l'atmosphère et renvoyé vers la surface
    alpha = mean_flux_top / flux_emis_terre
    return alpha
