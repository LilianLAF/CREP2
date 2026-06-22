# Projet Climat 2026 — Modèle 3

Ce modèle est la combinaison du Modèle 2.1 et du Modèle 2.2.

Le coefficient `alpha` (rapport flux sortant atmosphère / flux émis par la Terre) dépend à la fois :
- de **l'année** : concentrations en GES variables dans le temps (CO₂, CH₄, O₃, N₂O, H₂O) — comme dans le Modèle 2.1 ;
- de **l'altitude** : profil vertical de concentration calculé via le modèle atmosphérique US1976 — comme dans le Modèle 2.2.

Il s'agit du modèle le plus complet du projet.

## Utilisation

Depuis ce dossier :
```
python MAIN.py
```
Les sorties (graphique PNG + tableau CSV) sont sauvegardées dans `resultats/`.
