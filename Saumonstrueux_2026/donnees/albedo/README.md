# donnees/albedo

Albédos mensuels de surface issus des données CERES EBAF (satellite Terra/Aqua).

- `albedo01.csv` … `albedo12.csv` : albédo moyen mensuel (janvier à décembre) en 2023.
  - Première ligne : liste des latitudes.
  - Première colonne : liste des longitudes.
  - Valeur à l'intersection : albédo moyen du mois correspondant.
- `CERES_EBAF-TOA_Ed4.2.1_Subset_202401-202501.nc` : fichier source NetCDF CERES.

Les CSV ont été construits via les scripts `construction_csv.py` et `remplissage_csv.py` à partir du NetCDF.
