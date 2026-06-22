# Projet Climat 2026 — Saumonstrueux

Ce dossier suit le format de rendu demandé :

- `README.md` (ce document)
- `synthese.pdf` (à déposer ici)
- Code source dans les dossiers de chaque modèle
- Données communes dans `donnees/` (séparé du code)

## Arborescence

```
Saumonstrueux_2026/
├── donnees/                        # Données partagées (albedo, shapefiles, Cp, npy...)
│   └── Cp_humidity/
│       └── Implementation_RZSM_Chevreaux/   # Implémentation Cp spatiale (Carcajous Callipyges)
├── resultats/                      # Résultats de comparaison inter-modèles
├── Modèle squelette/               # Base simplifiée pour les années suivantes
├── Modèle 1/                       # Chevreaux brillants + Cp/Evap Carcajous Callipyges
│   ├── MAIN.py
│   ├── README.md
│   ├── resultats/                  # Sorties du modèle (PNG, CSV)
│   └── modules/                    # Fonctions du modèle
├── Modèle 2.1/                     # Modèle 1 + alpha = f(année)
│   ├── MAIN.py
│   ├── README.md
│   ├── resultats/
│   └── modules/
├── Modèle 2.2/                     # Modèle 1 + alpha = f(altitude)
│   ├── MAIN.py
│   ├── README.md
│   ├── resultats/
│   └── modules/
└── Modèle 3/                       # Modèle 2.1 + 2.2 : alpha = f(année, altitude)
    ├── MAIN.py
    ├── README.md
    ├── resultats/
    └── modules/
```

## Lancer un modèle

Depuis le dossier du modèle choisi :

```powershell
python MAIN.py
```

Le script demande latitude, longitude, et année (sauf Modèle 2.2).  
Les sorties (graphique PNG + tableau CSV) sont enregistrées dans `resultats/`.

## Données

Toutes les données sont centralisées dans `donnees/` :
- `albedo/` — albédos mensuels (CERES)
- `Cp_humidity/` — humidité du sol RZSM + implémentation spatiale
- `map/` — shapefiles pays (Natural Earth)
- `data/` — shapefiles côtes (Natural Earth)
- `npy/` — profils atmosphériques
