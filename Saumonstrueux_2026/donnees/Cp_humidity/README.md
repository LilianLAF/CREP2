# donnees/Cp_humidity

Données d'humidité du sol utilisées pour calculer la capacité thermique volumique de la surface.

- `average_rzsm_tout.csv` : grille mondiale d'humidité de la zone racinaire (Root Zone Soil Moisture, RZSM) à résolution 1°×1°. Colonnes : `lon`, `lat`, `RZSM`.

Utilisé par `parametrage_surface.py` de chaque modèle pour calculer la capacité thermique Cp en fonction de la position géographique (modèle Carcajous Callipyges).
