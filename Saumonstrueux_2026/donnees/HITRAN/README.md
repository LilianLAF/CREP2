# donnees/HITRAN

Données et script de traitement des sections efficaces d'absorption des gaz à effet de serre, issues de la base de données **HITRAN**.

## Fichiers

- `section_efficace.py` : script de traitement des données HITRAN. Lit le fichier `.par`, construit les spectres d'absorption par binning, puis ajuste un modèle analytique log-linéaire pour chaque GES (CO₂, CH₄, O₃, N₂O, H₂O). Produit les fonctions `cross_section_XXX(wavelength)` utilisées dans `atmosphere/Code_atmo_couche_backup.py`.
- `6a2ad240.par` : fichier source HITRAN2004 (**à placer ici manuellement**, non versionné car volumineux). Téléchargeable depuis [hitran.org](https://hitran.org). Contient les raies d'absorption pour H₂O (1), CO₂ (2), O₃ (3), N₂O (4), CO (5), CH₄ (6), O₂ (7).

## Utilisation

Placer `6a2ad240.par` dans ce dossier, puis exécuter depuis ce dossier :

```
python section_efficace.py
```

Le script affiche les coefficients `(a, b, lambda0)` du modèle ajusté pour chaque gaz. Ces valeurs sont ensuite à reporter dans `atmosphere/Code_atmo_couche_backup.py`.

## Modèle analytique ajusté

$$\sigma(\lambda) = 10^{\,a \;-\; b \cdot |\lambda - \lambda_0| / \lambda_0}$$

| Gaz | λ₀ (µm) |
|---|---|
| CO₂ | 15.0 |
| O₃ | 9.6 |
| N₂O | 17.0 |
| H₂O | 6.3 |
| CH₄ | double bande |
