# Tableau de Bord Académique

Application web interactive pour le suivi des performances académiques des étudiants, développée avec Python et Dash.

## Description

Ce tableau de bord académique permet aux enseignants et administrateurs de suivre facilement les performances individuelles des étudiants à travers une interface interactive et des visualisations dynamiques. L'application offre une vue d'ensemble des notes par matière, des comparaisons avec les moyennes de classe, et des statistiques par unité d'enseignement.

## Fonctionnalités

- **Sélection d'étudiant** via menu déroulant
- **Filtrage par Unité d'Enseignement**
- **Statistiques globales** (moyenne générale, nombre de matières)
- **Visualisations interactives**:
  - Performance par matière avec comparaison à la moyenne de classe
  - Répartition des moyennes par UE
- **Interface responsive** avec design Bootstrap
- **Gestion robuste des données** issues de fichiers Excel

## Prérequis

- Python 3.7+
- Bibliothèques Python (voir `requirements.txt`)

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/votre-username/tableau-de-bord-academique.git
   cd tableau-de-bord-academique
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

1. Placez votre fichier de données Excel dans le dossier du projet (structure requise décrite ci-dessous).

2. Lancez l'application :
   ```bash
   python app.py
   ```
   
   Ou spécifiez un fichier de données personnalisé :
   ```bash
   python app.py chemin/vers/votre/fichier.xlsx
   ```

3. Ouvrez votre navigateur à l'adresse : `http://127.0.0.1:8050/`

## Structure du fichier Excel

Le fichier Excel doit contenir les colonnes suivantes :
- `Nom` : nom de famille de l'étudiant
- `Prenom` : prénom de l'étudiant
- `Matière` : intitulé du cours
- `Note` : note obtenue sur 20
- `UE` : unité d'enseignement

## Structure du projet

```
tableau-de-bord-academique/
├── app.py                # Application principale
├── data_tdb.xlsx         # Exemple de fichier de données
├── requirements.txt      # Dépendances Python
└── README.md             # Ce fichier
```

## Exigences

```
dash==2.9.0
dash-bootstrap-components==1.4.0
pandas==1.5.3
plotly==5.14.0
openpyxl==3.1.2
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.
