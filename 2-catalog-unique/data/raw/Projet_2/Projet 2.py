import pandas as pd


catalog_fr = pd.read_csv(r"C:\Users\NASSIM\Desktop\DATACLEANSING\catalog_fr.csv")
catalog_us = pd.read_csv(r"C:\Users\NASSIM\Desktop\DATACLEANSING\catalog_us.csv")
mapping_cat = pd.read_csv(r"C:\Users\NASSIM\Desktop\DATACLEANSING\mapping_categories.csv") 

def clean_columns(df):
    df.columns = df.columns.str.strip().str.lower()
    return df

catalog_fr = clean_columns(catalog_fr)
catalog_us = clean_columns(catalog_us)
mapping_cat = clean_columns(mapping_cat)


cols_needed = ['sku', 'name', 'category', 'weight', 'weight_unit', 'price', 'currency']
catalog_fr = catalog_fr[cols_needed]
catalog_us = catalog_us[cols_needed]

#  Concaténation

catalog = pd.concat([catalog_fr, catalog_us], ignore_index=True)
print("Catalogue combiné :", len(catalog), "produits")

#  Nettoyage des textes

def clean_text(text):
    if pd.isna(text):
        return None
    return str(text).strip()

catalog['name'] = catalog['name'].apply(clean_text)
catalog['category'] = catalog['category'].apply(clean_text)

#  Poids en kg

def convert_weight(row):
    if pd.isna(row['weight']):
        return None
    try:
        w = float(row['weight'])
        unit = str(row['weight_unit']).lower()
        if unit in ['g', 'gram', 'grams']:
            return w / 1000
        elif unit in ['kg', 'kilogram', 'kilograms']:
            return w
        elif unit in ['lb', 'lbs', 'pound', 'pounds']:
            return w * 0.453592
        else:
            return w
    except:
        return None

catalog['weight_kg'] = catalog.apply(convert_weight, axis=1)


#  Prix en €

def convert_price(row):
    if pd.isna(row['price']):
        return None
    try:
        p = float(row['price'])
        if str(row['currency']).upper() == 'USD':
            return round(p * 0.93, 2)  # taux USD -> EUR
        return p
    except:
        return None

catalog['price_eur'] = catalog.apply(convert_price, axis=1)


#  Mapping des catégories

catalog = catalog.merge(mapping_cat, how='left', left_on='category', right_on='source_category')
catalog['category_canonique'] = catalog['target_category'].fillna('Non défini')
catalog.drop(['source_category','target_category'], axis=1, inplace=True)


#  Suppression des doublons exacts sur SKU

catalog_clean = catalog.drop_duplicates(subset=['sku'])
print("Après suppression des doublons exacts :", len(catalog_clean), "produits")


kpi = {
    'total_produits': len(catalog),
    'doublons_SKU_supprimes': len(catalog) - len(catalog_clean),
    'produits_sans_categorie': (catalog_clean['category_canonique'] == 'Non défini').sum(),
    'produits_sans_poids': catalog_clean['weight_kg'].isna().sum(),
    'produits_sans_prix': catalog_clean['price_eur'].isna().sum()
}


csv_clean = r"C:\Users\NASSIM\Desktop\DATACLEANSING\catalog_canonique.csv"
csv_kpi = r"C:\Users\NASSIM\Desktop\DATACLEANSING\kpi_catalog.csv"

catalog_clean.to_csv(csv_clean, index=False)
pd.DataFrame([kpi]).to_csv(csv_kpi, index=False)

print("Catalogue canonique généré :", csv_clean)
print("KPI généré :", csv_kpi)
print("KPI :", kpi)
