# Modèle squelette

Version simplifiée du modèle de température de surface, sans paramétrage géographique ni effet de serre.

Destiné aux groupes des années suivantes comme point de départ minimal. Les constantes (Cp, albédo, alpha…) sont hardcodées et doivent être remplacées par des modules plus élaborés.

## Fichiers

- `MAIN.py` : script principal, directement exécutable.
- `librairie_puissances.py` : fonctions de calcul des puissances surfaciques.
- `Visualisation.py` : tracé de la courbe de température.
- `Code_émission_simple` : code de référence simplifié.
- `temperature_48.0N_2.0E_2024.csv` : exemple de données de température mesurées (Paris, 2024).

## Utilisation

```
python MAIN.py
```
