# Streamlit Planes

## Maquette et tableau de bord
Maquette: 
Lien vers le canva du projet: 
https://www.canva.com/design/DAG0h-cJldE/1JMorxKJ5N7iW6EYFygqSg/edit?utm_content=DAG0h-cJldE&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

Lien du tableau de bord:
https://docs.google.com/spreadsheets/d/1DRsLZsDgtIq24xRAVeFb97EdK79zu5jTzrBYcnUoi5U/edit?usp=sharing

## Présentation générale et fonctionnement

Streamlit Planes est une application interactive développée avec Streamlit pour analyser les données de l'aviation européenne. L'application permet d'explorer les flux aériens (vols et passagers), les émissions de CO₂ liées à l'aviation, et d'effectuer des comparaisons entre pays européens. Elle utilise des données officielles d'Eurostat et d'Our World in Data pour fournir une visualisation claire et interactive des tendances dans le domaine de l'aviation.

## Arborescence du projet des fichiers importants

```
streamlit-planes/
├── app.py
├── barchart.py
├── functions.py
├── linechart.py
├── map.py
└── script/
    ├── list_iso.py
    ├── traitement_aeroport.py
    ├── traitement_co2.ipynb
    └── traitement_passagers_pays.ipynb
```

## Bibliothèques nécessaires pour le projet

- streamlit
- pandas
- numpy
- plotly
- geopandas

## Résumé catégories par catégories

### Backend
- `app.py`: Point d'entrée principal de l'application Streamlit
- `functions.py`: Fonctions utilitaires pour le traitement des données
- `script/`: Scripts de traitement des données brutes

### Visualisations
- `barchart.py`: Génération des graphiques en barres
- `linechart.py`: Génération des graphiques en lignes
- `map.py`: Visualisation cartographique des données

### Données
- `script/traitement_aeroport.py`: Traitement des données des aéroports
- `script/traitement_co2.ipynb`: Traitement des données d'émissions CO₂
- `script/traitement_passagers_pays.ipynb`: Traitement des données de passagers par pays

## Comment lancer le projet

1. Cloner le dépôt
2. Installer les dépendances avec `pip install -r requirements.txt`
3. Lancer l'application avec `streamlit run app.py`

> Informations à compléter: Vérifier que les fichiers de données nécessaires sont présents dans le dossier `data/`

## API

L'application utilise des données publiques provenant d'Eurostat et d'Our World in Data. Les données sont pré-traitées et stockées dans des fichiers CSV.

## Cas d'usage

- Analyse comparative des flux aériens entre pays européens
- Visualisation des émissions de CO₂ liées à l'aviation
- Identification des aéroports les plus fréquentés
- Exploration des tendances de trafic passagers

## Structure des données

Les données principales incluent:
- Flux aériens (vols arrivées/départs)
- Passagers par aéroport et par pays
- Émissions de CO₂ liées à l'aviation

## Avertissements et limitations

- Les données sont limitées aux pays européens
- Les visualisations sont basées sur des données annuelles
- Certaines fonctionnalités nécessitent une connexion Internet pour charger les données
- Les données de CO₂ sont approximatives et peuvent varier selon les sources