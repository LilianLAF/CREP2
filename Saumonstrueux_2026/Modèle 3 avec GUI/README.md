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


## Lancement du programme 
 Créer un environnement virtuel .\.venv (version quelconque)
 activer l'environnement virtuel avec .\.venv\Scripts\Activate.ps1
    Si erreur dû a la sécurité, utiliser la commande : Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
 Puis installer les bibliothèques du Requirements avec : pip install -r Requirements.txt
    Si erreur, alors se déplacer dans le bon dossier et reprendre a partir de l'activation de l'environnement virtuel
Exécuter le fichier Main.py sur le Modèle sans GUI
Ou
Exécuter le fichier GUI.py sur le modèle avec GUI