import pandas as pd
import re
import pycountry


csv_input = r"C:\Users\NASSIM\Desktop\DATACLEANSING\clients.csv"
df = pd.read_csv(csv_input)
print("Fichier original chargé :", len(df), "lignes")


#  Fonctions de nettoyage

def clean_email(email):
    if pd.isna(email):
        return None
    email = email.strip().lower()
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return email
    return None

def clean_phone(phone):
    if pd.isna(phone):
        return None
    phone = re.sub(r'\D', '', str(phone))
    if len(phone) < 7:
        return None
    return phone

def clean_birthdate(date):
    try:
        return pd.to_datetime(date, errors='coerce').date()
    except:
        return None

def normalize_country(country):
    if pd.isna(country):
        return None
    country = country.strip().lower()
    manual_mapping = {
        "fr": "France", "fra": "France",
        "ch": "Switzerland", "suisse": "Switzerland",
        "uk": "United Kingdom", "gb": "United Kingdom",
        "usa": "United States", "us": "United States",
        "de": "Germany", "esp": "Spain", "es": "Spain"
    }
    if country in manual_mapping:
        return manual_mapping[country]
    country_names = [c.name for c in pycountry.countries]
    # Correspondance approximative simple
    for name in country_names:
        if country in name.lower():
            return name
    return country.title()


#  KPI avant nettoyage

kpi = {}
kpi['total_lignes'] = len(df)
kpi['emails_invalides'] = df['email'].apply(lambda x: 0 if clean_email(x) else 1).sum()
kpi['telephones_invalides'] = df['telephone'].apply(lambda x: 0 if clean_phone(x) else 1).sum()
kpi['doublons_exact'] = df.duplicated(subset=['email', 'telephone']).sum()


#  Nettoyage

df['email'] = df['email'].apply(clean_email)
df['telephone'] = df['telephone'].apply(clean_phone)
df['pays'] = df['pays'].apply(normalize_country)
df['naissance'] = df['naissance'].apply(clean_birthdate)


#  Suppression des doublons exacts

df_clean = df.drop_duplicates(subset=['email', 'telephone'])
print("Après suppression des doublons exacts :", len(df_clean), "lignes")


#  KPI après nettoyage

kpi['total_lignes_apres'] = len(df_clean)
kpi['emails_invalides_apres'] = df_clean['email'].isna().sum()
kpi['telephones_invalides_apres'] = df_clean['telephone'].isna().sum()
kpi['doublons_exact_supprimes'] = kpi['total_lignes'] - kpi['total_lignes_apres']


# 7. Sauvegarde des fichiers

csv_clean = r"C:\Users\NASSIM\Desktop\DATACLEANSING\clients_clean.csv"
csv_kpi = r"C:\Users\NASSIM\Desktop\DATACLEANSING\kpi_qualite.csv"

df_clean.to_csv(csv_clean, index=False)
pd.DataFrame([kpi]).to_csv(csv_kpi, index=False)

print("Nettoyage terminé !")
print(f"Fichier clients_clean.csv généré : {csv_clean}")
print(f"Fichier KPI généré : {csv_kpi}")
print("KPI :", kpi)
