from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import sys

sys.stdout.reconfigure(encoding="utf-8")

base_dir = Path(__file__).resolve().parent.parent
candidate_paths = [
    base_dir / "data" / "firstfich.xlsx",
    Path.cwd() / "data" / "firstfich.xlsx",
]

excel_path = next((p for p in candidate_paths if p.exists()), candidate_paths[0])

if not excel_path.exists():
    raise FileNotFoundError(f"Fichier Excel introuvable : {excel_path}")

print(f"Fichier chargé : {excel_path}")
df = pd.read_excel(excel_path)

print("\nAperçu des données :")
print(df.head())

print("\nDimensions du fichier :")
print(df.shape)

print("\nInformations générales :")
df.info()

print("\nDernières lignes :")
print(df.tail())

print("\nNoms des colonnes :")
print(df.columns.tolist())

print("\nStatistiques descriptives :")
print(df.describe(include="all"))

numeric_cols = df.select_dtypes(include="number").columns.tolist()
if numeric_cols:
    print("\nMoyennes par colonne numérique :")
    print(df[numeric_cols].mean())

print("\nValeures manquantes :")
print(df.isnull().sum())
#inssull (case vide)   

print("\nLignes avec Sales manquant :")
print(df[df["Sales"].isnull()])

print("\nLignes avec Postal Code manquant :")
print(df[df["Postal Code"].isnull()])

print("\nNombre de doublons :")
print(df.duplicated().sum())

df_clean = df.copy()
# supprimé les Sales manquantes
df_clean = df_clean.dropna(subset=["Sales"])

print(df_clean.isnull().sum())

print(df.shape)

print(df_clean.shape)

# Chiffre d'affaires total
total_sales = df_clean["Sales"].sum()
print(f"Chiffre d'affaires total : {total_sales:.2f} $")


sales_by_category = (
    df_clean.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(sales_by_category)



sales_by_region = (
    df_clean.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(sales_by_region)


top_products = (
    df_clean.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_products)

top_customers = (
    df_clean.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
                 )

print("\nTop 10 clients :")
print(top_customers)


sales_by_segment = (
    df_clean.groupby("Segment")["Sales"]
    .sum()
    .sort_values(ascending=False)
                     )

print("\nVentes par segment :")
print(sales_by_segment)


print(df_clean["Order Date"].dtype)
df_clean["Order Date"] = pd.to_datetime(df_clean["Order Date"])
df_clean["Year"] = df_clean["Order Date"].dt.year

sales_by_year = (
    df_clean.groupby("Year")["Sales"]
    .sum()
    .sort_index()
)

print("\nVentes par année :")
print(sales_by_year)


growth = sales_by_year.pct_change() * 100
#compare chaque année à l'année précédente.  Puis transforme le résultat en pourcentage.

print("\nCroissance annuelle :")
print(growth)



df_clean["Month"] = df_clean["Order Date"].dt.to_period("M")


monthly_sales = (
    df_clean.groupby("Month")["Sales"]
    .sum()
    .sort_index()
)

print("\nVentes par mois :")
print(monthly_sales)

#Quels sont les mois qui ont généré le plus de CA ?
top_months = monthly_sales.sort_values(ascending=False).head(10)

print("\nTop 10 des mois :")
print(top_months)

#  une chose importante : .sort_index()  classe chronologiquement.
# .sort_values(ascending=False) : classe selon le montant des ventes.

#-------------------------------------------------------------------------
plt.figure(figsize=(12, 5))

plt.plot(
    monthly_sales.index.astype(str),
    monthly_sales.values
         )

plt.title("Évolution mensuelle du chiffre d'affaires")
plt.xlabel("Mois")
plt.ylabel("Chiffre d'affaires ($)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()



df_clean["Month_Number"] = df_clean["Order Date"].dt.month

sales_by_month_number = (
    df_clean.groupby("Month_Number")["Sales"]
    .sum()
    .sort_values(ascending=False)
                        )

print("\nVentes cumulées par mois de l'année :")
print(sales_by_month_number)


sales_category_year = (
    df_clean.groupby(["Year", "Category"])["Sales"]
    .sum()
    .unstack()
    # .unstack() transforme le résultat en tableau beaucoup plus lisible.
                      )

print("\nVentes par année et catégorie :")
print(sales_category_year)


category_growth = (
    sales_category_year.loc[2018] / sales_category_year.loc[2015] - 1
                   ) * 100

print("\nCroissance des catégories entre 2015 et 2018 :")
print(category_growth.sort_values(ascending=False))
# De combien chaque catégorie a-t-elle progressé entre 2015 et 2018 ?

# Entre 2015 et 2018, Office Supplies affiche la plus forte croissance du chiffre d'affaires (+60,77 %), devant Technology (+55,00 %) et Furniture (+35,68 %). 
# Technology demeure néanmoins la catégorie générant le chiffre d'affaires le plus élevé en 2018, avec environ 269 k$.

sales_region_category = (
    df_clean.groupby(["Region", "Category"])["Sales"]
    .sum()
    .unstack()
                         )

print("\nVentes par région et catégorie :")
print(sales_region_category)

print("\nNombre de produits différents :")
print(df_clean["Product Name"].nunique())

top_products = (
    df_clean.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 produits :")
print(top_products)

bottom_products = (
    df_clean.groupby("Product Name")["Sales"]
    .sum()
    .sort_values()
    .head(10)
)

print("\nBottom 10 produits :")
print(bottom_products)

# ==========================================
# ANALYSE DES COMMANDES PAR PRODUIT
# ==========================================

orders_by_product = (
    df_clean.groupby("Product Name")["Order ID"]
    .nunique()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 produits par nombre de commandes :")
print(orders_by_product)


product_performance = (
    df_clean.groupby("Product Name")
    .agg(
        Sales=("Sales", "sum"),
        Orders=("Order ID", "nunique")
    )
)

product_performance["Sales_per_Order"] = (
    product_performance["Sales"] /
    product_performance["Orders"]
)

product_performance = product_performance.sort_values(
    "Sales",
    ascending=False
)

print("\nPerformance des produits :")
print(product_performance.head(10))



# ==========================================
# SEGMENTATION DES PRODUITS
# ==========================================

product_performance["Performance"] = "Faible"

product_performance.loc[
    (product_performance["Sales"] >= 10000) &
    (product_performance["Orders"] >= 5),
    "Performance"
] = "Élevée"

product_performance.loc[
    (product_performance["Sales"] >= 5000) &
    (product_performance["Orders"] >= 3) &
    (product_performance["Performance"] != "Élevée"),
    "Performance"
] = "Moyenne"

print("\nSegmentation des produits :")
print(product_performance.head(20))


performance_counts = product_performance["Performance"].value_counts()

print("\nNombre de produits par niveau de performance :")
print(performance_counts)


performance_percentage = (
    product_performance["Performance"]
    .value_counts(normalize=True)
    * 100
)
#value_counts() : donne le nombre.    Alors que : value_counts(normalize=True) : donne la proportion. et * 100 → transforme cette proportion en pourcentage.

print("\nPourcentage des produits par niveau :")
print(performance_percentage.round(2))



# ==========================================
# PRODUITS À FORTE VALEUR
# ==========================================

high_value_products = (
    product_performance
    .sort_values("Sales_per_Order", ascending=False)
    .head(10)
)

print("\nTop 10 produits par valeur moyenne par commande :")
print(high_value_products)


# ==========================================
# PRODUITS À FORTE FREQUENCE
# ==========================================

frequent_products = (
    product_performance
    .sort_values("Orders", ascending=False)
    .head(10)
)

print("\nTop 10 produits par nombre de commandes :")
print(frequent_products)


# ==========================================
# PRODUITS À FORTE PERFORMANCE COMMERCIALE
# ==========================================

best_products = (
    product_performance[
        (product_performance["Orders"] >= 5) &
        (product_performance["Sales"] >= 10000)
    ]
    .sort_values("Sales", ascending=False)
)

print("\nProduits à forte performance commerciale :")
print(best_products)


# ==========================================
# KPI PRINCIPAUX
# ==========================================

total_orders = df_clean["Order ID"].nunique()
total_customers = df_clean["Customer ID"].nunique()
total_products = df_clean["Product Name"].nunique()
average_order_value = total_sales / total_orders

print("\n========== KPI PRINCIPAUX ==========")
print(f"Chiffre d'affaires total : {total_sales:.2f} $")
print(f"Nombre de commandes : {total_orders}")
print(f"Nombre de clients : {total_customers}")
print(f"Nombre de produits : {total_products}")
print(f"Panier moyen : {average_order_value:.2f} $")