# Pistes d'amélioration

Ce document recense les améliorations identifiées mais non implémentées dans le cadre du CREP 2025-2026, classées par thème et par complexité croissante.

---

## 1. Modélisation atmosphérique

### 1.1 Profil vertical des GES
Les profils d'altitude de CO₂, CH₄, N₂O et O₃ sont actuellement des fonctions affines par morceaux ajustées manuellement. Des données mesurées existent (bases AFGL, MIPAS).

**Piste** : Charger les profils verticaux depuis des fichiers `.npy` (dossier `donnees/npy/`, actuellement vide) pour une représentation plus réaliste.


### 1.2 Rétroaction vapeur d'eau
Quand la température augmente, l'évaporation s'intensifie, ce qui accroît la concentration en H₂O atmosphérique et renforce l'effet de serre — c'est la principale rétroaction climatique positive.

**Piste** : Coupler la concentration en H₂O à la température de surface simulée via la relation de Clausius-Clapeyron.

---

## 2. Bilan énergétique de surface

### 2.1 Albédo dynamique
L'albédo est actuellement calculé une seule fois via l'API NASA POWER (moyenne sur 2 ans) et reste constant pendant toute la simulation. Or l'albédo varie avec la saison (couverture neigeuse, végétation).

**Piste** : Utiliser les données CERES déjà disponibles dans `donnees/albedo/` pour un albédo mensuel réaliste.

### 2.2 Rétroaction glace-albédo
La formation/fonte de glace modifie fortement l'albédo (glace ≈ 0,6 vs océan ≈ 0,06). Cette rétroaction est absente du modèle.

**Piste** : Conditionner l'albédo à la température de surface (transition sol/glace autour de 273 K).


### 2.3 Évaporation variable
Le flux d'évaporation est actuellement une constante par continent. Il devrait dépendre de la température de surface, de l'humidité et du vent.

**Piste** : Utiliser la formule de Penman-Monteith couplée à la température simulée.

---


## 3. Résolution spatiale

### 3.1 Simulation 2D (grille globale)
Le modèle simule un unique point géographique. Une extension naturelle serait une grille mondiale (par exemple 2,5° × 2,5°) avec interpolation des paramètres.

**Difficulté** : Le temps de calcul croît en O(N²) avec la résolution. Une parallélisation (multiprocessing ou GPU) serait nécessaire.


## 4. Architecture logicielle

### 4.1 Configuration centralisée
Les paramètres physiques (d, T0, T_air, dt, durée) sont codés en dur dans `MAIN.py`. Une amélioration serait un fichier de configuration `config.yml` lu au démarrage.

### 4.2 Tests unitaires
Aucun test automatisé n'existe. Des tests unitaires sur `P_inc_solar`, `planck_function` et `calcul_alpha` permettraient de détecter rapidement les régressions.

### 4.3 Interface utilisateur
L'entrée des paramètres par `input()` est fonctionnelle mais rudimentaire. Une interface graphique simple (Tkinter, Streamlit) ou un argument en ligne de commande (`argparse`) améliorerait l'ergonomie.
