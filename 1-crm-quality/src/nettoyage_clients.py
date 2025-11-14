import pandas as pd
import re
import os

print("🚀 DÉMARRAGE DU MINI-PROJET 1 - NETTOYAGE CLIENTS")
print("=" * 50)

# Chemins des fichiers
input_path = "../data/raw/clients.csv"
output_path = "../data/clean/clients_clean.csv"
report_path = "../reports/kpi_qualite_clients.csv"

# 1. CHARGEMENT DES DONNÉES
print("📁 Chargement des données...")
df = pd.read_csv(input_path)
print(f"✅ Données chargées : {len(df)} lignes")

# 2. NETTOYAGE DES DONNÉES
print("🧹 NETTOYAGE EN COURS...")

# Nettoyer les emails
df['email'] = df['email'].astype(str).str.strip().str.lower()

# Nettoyer les noms
df['nom'] = df['nom'].astype(str).str.strip().str.title()
df['prenom'] = df['prenom'].astype(str).str.strip().str.title()

# 3. SUPPRESSION DES DOUBLONS
lignes_avant = len(df)
df_clean = df.drop_duplicates(subset=['email'])
lignes_apres = len(df_clean)

# 4. SAUVEGARDE
os.makedirs(os.path.dirname(output_path), exist_ok=True)
os.makedirs(os.path.dirname(report_path), exist_ok=True)
df_clean.to_csv(output_path, index=False)

# 5. RAPPORT
kpi = {'lignes_avant': lignes_avant, 'lignes_apres': lignes_apres}
pd.DataFrame([kpi]).to_csv(report_path, index=False)

print("🎉 NETTOYAGE TERMINÉ !")
print(f"📊 {lignes_apres} lignes nettoyées")
