# Configuration VS Code — CREP2

Ce dossier contient la configuration locale de l'éditeur VS Code pour le projet.
Les fichiers ici ne font pas partie du code livré : ils servent uniquement à améliorer
l'expérience de développement.

---

## `settings.json`

### `python.analysis.extraPaths`

Indique à l'analyseur Python (Pylance) où chercher les modules du projet,
afin de résoudre les imports et d'activer l'autocomplétion dans VS Code.

| Chemin ajouté | Pourquoi |
|---------------|----------|
| `Modèle 1/modules/bilan_energetique` | Accès direct aux sous-modules `librairie_puissances`, `parametrage_surface`, etc. |
| `Modèle 1/modules/atmosphere` | Accès direct à `transfert_radiatif`, `fonction_calcul_alpha` |
| `Modèle 3/modules` | Résolution des imports de package (`from bilan_energetique import ...`) |

> Ces chemins n'affectent pas l'exécution Python — ils servent uniquement à VS Code
> pour la navigation et la détection d'erreurs statiques.

### Modifier ce fichier

Pour ajouter un modèle (ex. Modèle 2.1) à l'analyse statique :

```json
"python.analysis.extraPaths": [
    "./Saumonstrueux_2026/Modèle 2/Modèle 2.1/modules/bilan_energetique",
    "./Saumonstrueux_2026/Modèle 2/Modèle 2.1/modules/atmosphere",
    ...
]
```
