# Projet Climat 2026

Ce dossier suit le format de rendu demande:

- `README.md` (ce document)
- `synthese.pdf` (a deposer ici)
- code source dans des dossiers separes par modele
- donnees lourdes dans un dossier separe du code: `donnees/`

## Arborescence utile

- `Modèle 1/` : version de base executable via `MAIN.py`
- `Modèle 2/` : version enrichie executable via `MAIN.py`
- `donnees/` : donnees communes (albedo, Cp_humidity, shapefiles, npy, etc.)

## Lancer les modeles

Depuis le dossier du modele choisi:

```powershell
python MAIN.py
```

Le script demande:

- latitude
- longitude
- annee

## Notes d'organisation

- Les chemins de donnees ont ete unifies vers `insereznomgroupe_2026/donnees/`.
- Le dossier `Modèle 2/ressources/` est conserve comme archive technique, mais les executions principales utilisent `donnees/`.
