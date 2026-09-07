# Hajer & Yassine — faire-part de mariage

Invitation de mariage numérique, page web autonome partageable par lien.

**Lundi 26 octobre 2026** · cérémonie à 20h30 · Salle des fêtes Top Happiness, Les Berges du Lac (Tunis).

Style beylical (dorures, faste ottoman, palette bordeaux + or) : porte de palais qui s'ouvre
au toucher, salon doré, mot des mariés, sceau de cire à toucher pour révéler la date, lieu avec
itinéraire, remerciements — le tout avec une musique originale (piano + cordes + percussion douce)
et un bouton pour la couper.

## Fichiers

- [`index.html`](index.html) — la page finale, **autonome** (les photos sont intégrées en
  data URI, la musique est synthétisée dans la page). C'est le seul fichier à ouvrir ou héberger ;
  nommé `index.html` pour être servi à la racine par GitHub Pages.
- [`src/invitation.tpl.html`](src/invitation.tpl.html) — le gabarit source (marqueurs `%%IMG_*%%`).
- [`src/build.py`](src/build.py) — reconstruit `index.html` en réencodant les photos et en
  mesurant l'ouverture de la porte pour animer les battants.
- [`src/assets/`](src/assets) — les trois photos sources (porte fermée, salon, embrasure ouverte).

## Reconstruire

```bash
pip install opencv-python-headless numpy
cd src && python build.py
```

Pour changer les photos, remplacer les fichiers de `src/assets/` (mêmes noms, format vertical 9:16
de préférence) puis relancer `build.py`.
