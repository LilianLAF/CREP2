# CREP 2025-2026 — Groupe Saumonstrueux

Projet de modélisation climatique dans le cadre de l'UE **Transition Écologique et Développement Soutenable (TEDS)** — École Centrale de Lyon, 2ème année.

**Membres du groupe :**
Camille Simond · Maxence Lucas Morel · Bilel Bouchama · Elsa Mauron · Lilian Laffont · Mathéo Dhenaut · Vittoria Gelot · Anatole Ridereau · Lucas Poirot · Oïhana Daguerre · Isshac Taibi

**Encadrants :** M. Chevereau · M. Bernard

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

## Résultats clés (Modèle 3, année 2026)

- **OLR simulé :** 331,5 W/m² · **OLR GIEC (ciel clair) :** 267,0 W/m² · écart : +64,5 W/m²
- **α simulé :** 0,850 · **α GIEC :** 0,671 · écart : ~27 %
- **Forçage CO₂ × 2 simulé :** 3,19 W/m² · **référence Myhre (1998) :** 3,71 W/m² · écart : 13,9 %

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

## Références

- IPCC AR6 WGI, Figure 7.2 — Bilan énergétique de la Terre
- Myhre et al. (1998), *Geophys. Res. Lett.* — Forçage radiatif CO₂
- US Standard Atmosphere 1976 — Profils T(z), P(z)
- HITRAN Database — Sections efficaces d'absorption moléculaire
- Travaux des **Chevreaux Brillants** (2024-2025) et **Carcajous Callipyges** (2024-2025)