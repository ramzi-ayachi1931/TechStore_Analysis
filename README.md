# 📊 TechStore Analysis — Sales, Customer & Product Analytics

Projet complet d'analyse de données réalisé avec **Python, SQL et Power BI** à partir d'un jeu de données de ventes de type Superstore.

L'objectif est d'analyser la performance commerciale, le comportement des clients et la performance des produits afin d'identifier des tendances et des opportunités business.

---

## 🎯 Objectifs du projet

- Analyser l'évolution du chiffre d'affaires
- Identifier les catégories et sous-catégories les plus performantes
- Identifier les produits générant le plus de chiffre d'affaires
- Analyser la performance commerciale par région
- Étudier la valeur et le comportement des clients
- Réaliser une segmentation client avec la méthode RFM
- Construire un dashboard interactif avec Power BI

---

## 🛠️ Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python | Nettoyage et analyse des données |
| Pandas | Manipulation des données |
| SQL | Analyse et requêtes |
| SQLite | Stockage des données |
| Power Query | Transformation des données |
| DAX | Création des KPI et mesures |
| Power BI | Visualisation et dashboard |
| Excel | Source des données |

---

## 📊 Résultats clés

### Performance commerciale

- **Chiffre d'affaires total : 2,26 M$**
- **2015 : 479,33 K$**
- **2016 : 459,44 K$**
- **2017 : 599,49 K$**
- **2018 : 721,35 K$**

La croissance est particulièrement forte en 2017 et 2018.

### Performance par catégorie

- **Technology : 825,53 K$**
- **Furniture : 728,66 K$**
- **Office Supplies : 705,42 K$**

### Performance régionale

- **West : 710,22 K$**
- **East : 669,40 K$**
- **Central : 491,54 K$**
- **South : 388,45 K$**

---

## 👥 Analyse clients — RFM

Une segmentation RFM a été réalisée à partir de trois dimensions :

- **Recency** : nombre de jours depuis le dernier achat
- **Frequency** : nombre de commandes
- **Monetary** : chiffre d'affaires généré

### Segments identifiés

- 🏆 Champions
- ⭐ Clients fidèles
- 📈 Clients à potentiel
- 🔄 À réactiver
- ⚠️ À risque

Cette segmentation permet d'identifier les clients à forte valeur et ceux nécessitant des actions de fidélisation ou de réactivation.

---

## 📦 Analyse produits

L'analyse produits permet d'identifier :

- les produits générant le plus de chiffre d'affaires ;
- les catégories les plus performantes ;
- les sous-catégories les plus performantes ;
- l'évolution des ventes par catégorie.

---

# 📈 Dashboard Power BI

## 1. Analyse des ventes

![Analyse des ventes](screenshots/page1-analyse-ventes.png)

Vue globale de la performance commerciale : chiffre d'affaires, évolution des ventes, catégories et régions.

---

## 2. Analyse clients

![Analyse clients](screenshots/page2-analyse-clients.png)

Analyse de la segmentation RFM, des clients à forte valeur, du chiffre d'affaires par segment et de la récence des achats.

---

## 3. Analyse produits

![Analyse produits](screenshots/page3-analyse-produits.png)

Analyse des produits, catégories, sous-catégories et du chiffre d'affaires généré.

---

## 📁 Structure du projet

```text
TechStore_Analysis/
│
├── data/
│   ├── firstfich.xlsx
│   ├── sales.csv
│   └── customer_rfm.csv
│
├── database/
│   └── techstore.db
│
├── notebook/
│   └── analyse.py
│
├── screenshots/
│   ├── page1-analyse-ventes.png
│   ├── page2-analyse-clients.png
│   └── page3-analyse-produits.png
│
└── README.md