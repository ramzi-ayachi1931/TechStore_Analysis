from pathlib import Path
import pandas as pd
import sqlite3

# ==========================================
# 1. LOCALISATION DU FICHIER EXCEL
# ==========================================

base_dir = Path(__file__).resolve().parent.parent

excel_path = base_dir / "data" / "firstfich.xlsx"
database_path = base_dir / "database" / "techstore.db"

# Vérification
if not excel_path.exists():
    raise FileNotFoundError(
        f"Fichier Excel introuvable : {excel_path}"
    )

print(f"Fichier Excel : {excel_path}")


# ==========================================
# 2. CHARGEMENT DES DONNÉES
# ==========================================

df = pd.read_excel(excel_path)

print(f"Nombre de lignes : {len(df)}")
print(f"Nombre de colonnes : {len(df.columns)}")


# ==========================================
# 3. NETTOYAGE
# ==========================================

df_clean = df.dropna(subset=["Sales"]).copy()

print(f"Lignes après nettoyage : {len(df_clean)}")


# ==========================================
# 4. CONNEXION À SQLITE
# ==========================================

connection = sqlite3.connect(database_path)


# ==========================================
# 5. CRÉATION DE LA TABLE
# ==========================================

df_clean.to_sql(
    "sales",
    connection,
    if_exists="replace",
    index=False
)


# ==========================================
# 6. VÉRIFICATION
# ==========================================

cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM sales")

count = cursor.fetchone()[0]

print(f"Nombre de lignes dans SQL : {count}")


# ==========================================
# 7. FERMETURE
# ==========================================

connection.close()

print(f"\nBase SQL créée : {database_path}")