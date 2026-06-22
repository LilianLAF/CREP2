# Documentation — Saumonstrueux 2026

Ce dossier regroupe la documentation technique du projet CREP 2025-2026.
Il est distinct du code source et des données ; il sert de référence pour
comprendre les choix de modélisation et les axes d'évolution du projet.

---

## Contenu

### `Pistes d'amélioration/`
Recense les améliorations identifiées mais non implémentées faute de temps.
Organisé en thèmes :
- **Modélisation atmosphérique** — profils verticaux réels (AFGL/MIPAS), rétroaction H₂O, sections efficaces HITRAN
- **Bilan énergétique** — albédo dynamique (CERES), rétroaction glace-albédo, évaporation variable (Penman-Monteith)
- **Schéma numérique** — résolution temporelle, stabilité
- **Résolution spatiale** — passage d'un modèle 1D colonne à une grille 2D
- **Validation** — comparaison systématique avec ERA5 / CERES
- **Architecture logicielle** — tests unitaires, configuration centralisée

---

## Liens utiles

- Code source : `../Modèle 1/`, `../Modèle 2.1/`, `../Modèle 2.2/`, `../Modèle 3/`
- Données d'entrée : `../donnees/`
- Résultats graphiques : `../resultats/`
