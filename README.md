# nettoyage-donnees-projet
Projet de nettoyage de données - Qualité des données et automatisation
#  Projet de Nettoyage de Données

##  Description
Ce projet contient 3 mini-projets de nettoyage de données utilisant Python et Pandas pour améliorer la qualité des données clients, produits et ventes.

##  Mini-projets réalisés

### 1. CRM de Qualité Optimale (`1-crm-quality/`)
- **Objectif** : Nettoyer les données clients
- **Tâches** :
  - Standardisation des emails, pays, téléphones
  - Suppression des doublons
  - Validation des formats
- **Fichiers** :
  - `src/nettoyage_clients.py` - Code de nettoyage
  - `data/raw/clients.csv` - Données brutes
  - `data/clean/clients_clean.csv` - Données nettoyées
  - `reports/kpi_qualite.csv` - Indicateurs de qualité

### 2. Catalogue Produit Unique (`2-catalog-unique/`)
- **Objectif** : Fusionner et nettoyer les catalogues produits
- **Tâches** :
  - Fusion catalogues français et américain
  - Standardisation des catégories
  - Conversion des unités de poids
- **Fichiers** :
  - `src/nettoyage_catalog.py` - Code de nettoyage
  - `data/raw/catalog_fr.csv`, `catalog_us.csv` - Données brutes
  - `data/clean/catalog_canonique.csv` - Catalogue fusionné
  - `reports/kpi_catalog.csv` - Indicateurs de qualité

### 3. Suivi des Ventes Quotidien (`3-sales-tracking/`)
- **Objectif** : Analyser et nettoyer les données de ventes
- **Tâches** :
  - Standardisation des dates
  - Vérification des montants
  - Calcul du chiffre d'affaires quotidien
- **Fichiers** :
  - `src/nettoyage_ventes.py` - Code de nettoyage
  - `data/raw/sales.csv` - Données brutes
  - `data/clean/sales_clean.csv` - Données nettoyées
  - `reports/daily_revenue.csv` - CA quotidien
  - `reports/kpi_sales.csv` - Indicateurs de qualité

##  Équipe
- **Jihad Haliba** - Mini-projet 1 (Clients) et partie Ventes
- **[nassim nasfi]** - Mini-projet 2 (Catalogue) et partie Ventes

##  Installation et utilisation

### Prérequis
```bash
pip install -r src/requirements.txt