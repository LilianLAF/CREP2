# Modèle 2.1 — modules

Les fonctions sont organisées en 3 sous-packages, importés par `MAIN.py` via `sys.path`.

## bilan_energetique/
Calculs de puissances surfaciques et paramétrage de la surface.

| Fichier | Rôle |
|---|---|
| `librairie_puissances.py` | Puissances surfaciques (solaire, thermique, convection, évaporation) |
| `parametrage_surface.py` | Classification du sol, albédo, capacité thermique Cp spatiale (RZSM) |
| `parametrage_convection.py` | Coefficient de convection h en fonction de la position |

## atmosphere/
Modèle radiatif et calcul du coefficient α.

| Fichier | Rôle |
|---|---|
| `fonction_calcul_alpha.py` | Calcul de α dépendant de **l'année** (CO₂, CH₄, O₃, N₂O, H₂O variables dans le temps) |
| `Code_atmo_couche_backup.py` | Transfert radiatif multi-couches spectral (distribution verticale homogène) |

## visualisation/
Génération et sauvegarde des sorties.

| Fichier | Rôle |
|---|---|
| `Visualisation.py` | Tracé de la température + sauvegarde PNG/CSV dans `resultats/` |
| `ZZ_cp.py` | Carte mondiale de la capacité thermique Cp (script autonome) |
