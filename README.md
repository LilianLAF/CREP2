# CREP 2025-2026 — Groupe Saumonstrueux

Projet de modélisation climatique dans le cadre de l'UE **Transition Écologique et Développement Soutenable (TEDS)**.
---

## Objectif

Développer un modèle couplé radiatif–énergétique simulant l'évolution de la température de surface terrestre, en tenant compte de l'effet de serre via un transfert radiatif spectral multi-couches.

---

## Organisation du dépôt

```
CREP2/
├── Saumonstrueux_2026/       ← rendu principal 2026
│   ├── Modèle 1/             ← bilan énergétique (base Chevreaux Brillants + améliorations)
│   ├── Modèle 2.1/           ← + GES dépendants du temps (CO₂, CH₄, N₂O, O₃, H₂O)
│   ├── Modèle 2.2/           ← + GES dépendants de l'altitude
│   ├── Modèle 3/             ← fusion 2.1 + 2.2 (modèle le plus complet)
│   ├── Modèle squelette/     ← modèle minimal pour tests rapides
│   ├── donnees/              ← données d'entrée (albédo, humidité, profils atmosphériques)
│   ├── resultats/            ← sorties graphiques des simulations
│   └── documentation/        ← pistes d'amélioration, notes techniques
├── Travail retenu/           ← archives des rendus des années précédentes (référence)
├── Requirements.txt          ← dépendances Python
└── README.md                 ← ce fichier
```

---

## Progression des modèles

| Modèle | Nouveauté principale |
|--------|----------------------|
| Modèle 1 | Bilan énergétique complet (capacité thermique, évapotranspiration, albédo corrigé) |
| Modèle 2.1 | Concentrations des GES évoluant dans le temps |
| Modèle 2.2 | Concentrations des GES dépendant de l'altitude |
| Modèle 3 | Fusion temporel + altitude — modèle de référence pour les résultats |
| Modèle squelette | Modèle minimal sans API, pour tests et pédagogie |

---

## Installation

```bash
pip install -r Requirements.txt
```

Lancer une simulation (exemple Modèle 3) :

```bash
cd "Saumonstrueux_2026/Modèle 3"
python modules/MAIN.py
```

---