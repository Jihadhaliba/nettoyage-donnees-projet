import pandas as pd

file_sales = r"C:\Users\NASSIM\Desktop\DATACLEANSING\sales.csv"
sales = pd.read_csv(file_sales)

print("Fichier ventes chargé :", len(sales), "lignes")

sales.columns = sales.columns.str.strip().str.lower()

sales['order_date'] = pd.to_datetime(sales['order_date'], errors='coerce').dt.date


sales['amount'] = pd.to_numeric(sales['amount'], errors='coerce')
sales.loc[sales['amount'].isna(), 'amount'] = 0

#  Identifier les remboursements

if 'type' in sales.columns:
    sales['is_refund'] = sales['type'].str.lower() == 'refund'
else:
    sales['is_refund'] = sales['amount'] < 0


# Supprimer les doublons exacts sur order_id + customer_email
sales_clean = sales.drop_duplicates(subset=['order_id', 'customer_email'])



#  Calcul du chiffre d’affaires quotidien

daily_revenue = sales_clean.groupby('order_date').agg(
    total_sales = ('amount', lambda x: x[sales_clean.loc[x.index, 'is_refund']==False].sum()),
    total_refunds = ('amount', lambda x: x[sales_clean.loc[x.index, 'is_refund']==True].sum())
).reset_index()


# 5. KPI

kpi = {
    'total_transactions': len(sales),
    'transactions_nettoyees': len(sales_clean),
    'transactions_dupliquees_supprimees': len(sales) - len(sales_clean),
    'transactions_avec_montant_zero': (sales_clean['amount'] == 0).sum(),
    'transactions_remboursements': sales_clean['is_refund'].sum()
}


csv_clean = r"C:\Users\NASSIM\Desktop\DATACLEANSING\sales_clean.csv"
csv_daily = r"C:\Users\NASSIM\Desktop\DATACLEANSING\daily_revenue.csv"
csv_kpi = r"C:\Users\NASSIM\Desktop\DATACLEANSING\kpi_sales.csv"

sales_clean.to_csv(csv_clean, index=False)
daily_revenue.to_csv(csv_daily, index=False)
pd.DataFrame([kpi]).to_csv(csv_kpi, index=False)

print("Nettoyage terminé !")
print("Fichier sales_clean.csv :", csv_clean)
print("Fichier daily_revenue.csv :", csv_daily)
print("Fichier KPI :", csv_kpi)
print("KPI :", kpi)
