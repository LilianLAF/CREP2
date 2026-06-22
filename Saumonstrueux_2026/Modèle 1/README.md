# Projet Climat 2026 — Modèle 1

Ce modèle est la combinaison des meilleures modélisations des groupes de 2024-2025.

Il prend comme base le code des **Chevreaux brillants**, auquel ont été intégrés plusieurs éléments du groupe des **Carcajous Callipyges** :

- **Capacité thermique** : valeurs d'humidité du sol spatialisées (RZSM, dépendant de la position), remplaçant les anciennes constantes par continent.
- **Évapotranspiration** : reprise directement des Carcajous Callipyges sans modification.
- **Découpage géographique du monde** : grille issue des Carcajous Callipyges.

Corrections apportées au code des Chevreaux brillants :
- Gestion des années corrigée.
- Correction d'`alpha` dans `librairie_puissances` (anciennement incohérent physiquement).
- Profondeur de surface terrestre fixée à **0.39 m** (cf. ex. 1, Chapitre 11).

Le coefficient `alpha` (rapport flux sortant atmosphère / flux émis par la Terre) est fixe dans ce modèle.

## Utilisation

Depuis ce dossier :
```
python MAIN.py
```
Les sorties (graphique PNG + tableau CSV) sont sauvegardées dans `resultats/`.
