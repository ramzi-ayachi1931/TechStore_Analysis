import sqlite3
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding="utf-8")

# ==========================================
# CONNEXION À LA BASE
# ==========================================

base_dir = Path(__file__).resolve().parent.parent
database_path = base_dir / "database" / "techstore.db"

connection = sqlite3.connect(database_path)
cursor = connection.cursor()


# ==========================================
# KPI : CA TOTAL
# ==========================================

query = """
SELECT SUM(Sales) AS total_sales
FROM sales;
        """

cursor.execute(query)

result = cursor.fetchone()

print(f"Chiffre d'affaires total : {result[0]:,.2f} $")


# ==========================================
# KPI : NOMBRE DE COMMANDES ET CLIENTS
# ==========================================

query = """
SELECT
    COUNT(DISTINCT "Order ID") AS total_orders,
    COUNT(DISTINCT "Customer ID") AS total_customers
FROM sales;
"""

cursor.execute(query)

result = cursor.fetchone()

print(f"Nombre de commandes : {result[0]}")
print(f"Nombre de clients : {result[1]}")


# ==========================================
# ANALYSE : CA PAR CATÉGORIE
# ==========================================

query = """
SELECT
    Category,
    SUM(Sales) AS total_sales
FROM sales
GROUP BY Category
ORDER BY total_sales DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

print("\nCA par catégorie :")

for row in rows:
    print(f"{row[0]} : {row[1]:,.2f} $")

 # ==========================================
# ANALYSE : CA PAR RÉGION
# ==========================================

query = """
SELECT
    Region,
    SUM(Sales) AS total_sales
FROM sales
GROUP BY Region
ORDER BY total_sales DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

print("\nCA par région :")

for row in rows:
    print(f"{row[0]} : {row[1]:,.2f} $")


# ==========================================
# ANALYSE : CA PAR ANNÉE
# ==========================================

query = """
SELECT
    strftime('%Y', "Order Date") AS year,
    SUM(Sales) AS total_sales
FROM sales
GROUP BY year
ORDER BY year;
"""
# strftime('%Y', "Order Date") : Extraire l'année de la date.

cursor.execute(query)

rows = cursor.fetchall()

print("\nCA par année :")

for row in rows:
    print(f"{row[0]} : {row[1]:,.2f} $")


# ==========================================
# ANALYSE : CROISSANCE ANNUELLE
# ==========================================

query = """
WITH yearly_sales AS (
    SELECT
        strftime('%Y', "Order Date") AS year,
        SUM(Sales) AS total_sales
    FROM sales
    GROUP BY year
                    )


SELECT
    year,
    total_sales,
    LAG(total_sales) OVER (ORDER BY year) AS previous_year_sales,
    ROUND(
        (total_sales - LAG(total_sales) OVER (ORDER BY year))
        / LAG(total_sales) OVER (ORDER BY year) * 100,
        2
    ) AS growth_percentage
FROM yearly_sales
ORDER BY year;
"""
# WITH permet de créer une CTE (Common Table Expression).
# LAG() permet de récupérer la valeur de la ligne précédente.

cursor.execute(query)

rows = cursor.fetchall()

print("\nCroissance annuelle :")

for row in rows:
    year, sales, previous_sales, growth = row

    if growth is None:
        print(f"{year} : {sales:,.2f} $ | Première année")
    else:
        print(
            f"{year} : {sales:,.2f} $ | "
            f"Année précédente : {previous_sales:,.2f} $ | "
            f"Croissance : {growth:.2f}%"
             )

# ==========================================
# TOP 10 CLIENTS
# ==========================================

query = """
SELECT
    "Customer Name",
    SUM(Sales) AS total_sales,
    COUNT(DISTINCT "Order ID") AS total_orders,
    ROUND(
        SUM(Sales) / COUNT(DISTINCT "Order ID"),
        2
    ) AS average_order_value
FROM sales
GROUP BY "Customer Name"
ORDER BY total_sales DESC
LIMIT 10;
"""

cursor.execute(query)

rows = cursor.fetchall()

print("\nTop 10 clients :")

for row in rows:
    customer, sales, orders, average_order = row

    print(
        f"{customer} | "
        f"CA : {sales:,.2f} $ | "
        f"Commandes : {orders} | "
        f"Panier moyen : {average_order:,.2f} $"
    )


# ==========================================
# CA PAR CATÉGORIE
# ==========================================

query = """
SELECT
    Category,
    SUM(Sales) AS total_sales
FROM sales
GROUP BY Category
ORDER BY total_sales DESC;
"""

cursor.execute(query)

results = cursor.fetchall()

print("\nCA par catégorie :")

for category, total_sales in results:
    print(f"{category} : {total_sales:,.2f} $")
#La catégorie Technology génère le chiffre d'affaires le plus élevé. 
#Elle représente donc un levier commercial important pour l'entreprise.


# ==========================================
# CA PAR RÉGION
# ==========================================

query = """
SELECT
    Region,
    SUM(Sales) AS total_sales
FROM sales
GROUP BY Region
ORDER BY total_sales DESC;
"""

cursor.execute(query)

results = cursor.fetchall()

print("\nCA par région :")

for region, total_sales in results:
    print(f"{region} : {total_sales:,.2f} $")


# ==========================================
# CA PAR RÉGION ET CATÉGORIE
# ==========================================

query = """
SELECT
    Region,
    Category,
    SUM(Sales) AS total_sales
FROM sales
GROUP BY Region, Category
ORDER BY Region, total_sales DESC;
"""

cursor.execute(query)

results = cursor.fetchall()

print("\nCA par région et catégorie :")

for region, category, total_sales in results:
    print(f"{region} | {category} : {total_sales:,.2f} $")


# ==========================================
# PART DES CATÉGORIES DANS CHAQUE RÉGION
# ==========================================

query = """
SELECT
    Region,
    Category,
    SUM(Sales) AS category_sales,
    ROUND(
        SUM(Sales) * 100.0 /
        SUM(SUM(Sales)) OVER (PARTITION BY Region),
        2
    ) AS category_share
FROM sales
GROUP BY Region, Category
ORDER BY Region, category_share DESC;
"""

cursor.execute(query)

results = cursor.fetchall()

print("\nPart des catégories dans chaque région :")

for region, category, sales, share in results:
    print(
        f"{region} | {category} | "
        f"CA : {sales:,.2f} $ | "
        f"Part : {share:.2f}%"
    )


# ==========================================
# SEGMENTATION DES CLIENTS
# ==========================================

query = """
SELECT
    "Customer Name" AS customer_name,
    SUM(Sales) AS total_sales,
    COUNT(DISTINCT "Order ID") AS orders,
    SUM(Sales) / COUNT(DISTINCT "Order ID") AS average_order
FROM sales
GROUP BY "Customer Name"
ORDER BY total_sales DESC;
"""

cursor.execute(query)

results = cursor.fetchall()

print("\nPerformance des clients :")

for customer, sales, orders, average_order in results[:20]:
    print(
        f"{customer} | "
        f"CA : {sales:,.2f} $ | "
        f"Commandes : {orders} | "
        f"Panier moyen : {average_order:,.2f} $"
          )


# ==========================================
# SEGMENTATION DES CLIENTS PAR CA
# ==========================================

query = """
WITH customer_sales AS (
    SELECT
        "Customer Name" AS customer_name,
        SUM(Sales) AS total_sales
    FROM sales
    GROUP BY "Customer Name"
),

ranked_customers AS (
    SELECT
        customer_name,
        total_sales,
        NTILE(4) OVER (ORDER BY total_sales DESC) AS customer_segment
    FROM customer_sales
)

SELECT
    customer_name,
    total_sales,
    CASE
        WHEN customer_segment = 1 THEN 'VIP'
        WHEN customer_segment = 2 THEN 'Premium'
        WHEN customer_segment = 3 THEN 'Standard'
        ELSE 'Faible valeur'
    END AS segment
FROM ranked_customers
ORDER BY total_sales DESC;
"""

cursor.execute(query)

results = cursor.fetchall()

print("\nSegmentation des clients :")

for customer, sales, segment in results[:30]:
    print(
        f"{customer} | "
        f"CA : {sales:,.2f} $ | "
        f"Segment : {segment}"
          )

# ==========================================
# RÉPARTITION DES CLIENTS PAR SEGMENT
# ==========================================

query = """
WITH customer_sales AS (
    SELECT
        "Customer Name" AS customer_name,
        SUM(Sales) AS total_sales
    FROM sales
    GROUP BY "Customer Name"
),

segmented_customers AS (
    SELECT
        customer_name,
        total_sales,
        NTILE(4) OVER (ORDER BY total_sales DESC) AS quartile
    FROM customer_sales
                        )

SELECT
    CASE
        WHEN quartile = 1 THEN 'VIP'
        WHEN quartile = 2 THEN 'Premium'
        WHEN quartile = 3 THEN 'Standard'
        ELSE 'Faible valeur'
    END AS segment,
    COUNT(*) AS number_of_customers,
    ROUND(
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM segmented_customers),
        2
    ) AS percentage
FROM segmented_customers
GROUP BY segment
ORDER BY number_of_customers DESC;
"""

cursor.execute(query)

results = cursor.fetchall()

print("\n========== RÉPARTITION DES CLIENTS ==========")

for segment, number_of_customers, percentage in results:
    print(
        f"{segment} | "
        f"Clients : {number_of_customers} | "
        f"Part : {percentage:.2f}%"
         )

# ==========================================
# ANALYSE RFM
# ==========================================

query = """
WITH customer_rfm AS (
    SELECT
        "Customer Name" AS customer_name,

        -- Monetary
        SUM(Sales) AS monetary,

        -- Frequency
        COUNT(DISTINCT "Order ID") AS frequency,

        -- Recency
        MAX(date("Order Date")) AS last_order

    FROM sales
    GROUP BY "Customer Name"
                     ),

reference_date AS (
    SELECT MAX(date("Order Date")) AS max_date
    FROM sales
)

SELECT
    customer_name,
    monetary,
    frequency,
    last_order,

    julianday(
        (SELECT max_date FROM reference_date)
    ) - julianday(last_order) AS recency

FROM customer_rfm
ORDER BY monetary DESC;
"""

cursor.execute(query)

results = cursor.fetchall()

print("\n========== ANALYSE RFM ==========")

for customer, monetary, frequency, last_order, recency in results[:20]:

    print(
        f"{customer} | "
        f"CA : {monetary:,.2f} $ | "
        f"Commandes : {frequency} | "
        f"Dernière commande : {last_order} | "
        f"Recency : {int(recency)} jours"
    )
# ==========================================
# SCORE RFM
# ==========================================

query = """
WITH customer_rfm AS (

    SELECT
        "Customer Name" AS customer_name,

        SUM(Sales) AS monetary,

        COUNT(DISTINCT "Order ID") AS frequency,

        MAX(date("Order Date")) AS last_order

    FROM sales

    GROUP BY "Customer Name"
),

rfm_data AS (

    SELECT
        customer_name,
        monetary,
        frequency,
        last_order,

        CAST(
            julianday(
                (SELECT MAX(date("Order Date")) FROM sales)
            ) - julianday(last_order)
            AS INTEGER
        ) AS recency

    FROM customer_rfm
),

rfm_scores AS (

    SELECT
        *,
        
        NTILE(5) OVER (
            ORDER BY recency DESC
        ) AS recency_score,

        NTILE(5) OVER (
            ORDER BY frequency ASC
        ) AS frequency_score,

        NTILE(5) OVER (
            ORDER BY monetary ASC
        ) AS monetary_score

    FROM rfm_data
)

SELECT
    customer_name,
    monetary,
    frequency,
    recency,
    recency_score,
    frequency_score,
    monetary_score,

    CAST(recency_score AS TEXT)
    || CAST(frequency_score AS TEXT)
    || CAST(monetary_score AS TEXT)
    AS rfm_score

FROM rfm_scores

ORDER BY monetary DESC;
"""

cursor.execute(query)

results = cursor.fetchall()

print("\n========== SCORE RFM ==========")

for row in results[:20]:

    (
        customer,
        monetary,
        frequency,
        recency,
        r_score,
        f_score,
        m_score,
        rfm_score
    ) = row

    print(
        f"{customer} | "
        f"CA : {monetary:,.2f} $ | "
        f"Commandes : {frequency} | "
        f"Recency : {recency} jours | "
        f"RFM : {rfm_score}"
    )

# ==========================================
# SEGMENTATION RFM
# ==========================================

query = """
WITH customer_rfm AS (

    SELECT
        "Customer Name" AS customer_name,

        SUM(Sales) AS monetary,

        COUNT(DISTINCT "Order ID") AS frequency,

        CAST(
            julianday((SELECT MAX("Order Date") FROM sales))
            - julianday(MAX("Order Date"))
            AS INTEGER
        ) AS recency

    FROM sales

    GROUP BY "Customer Name"
),

rfm_scores AS (

    SELECT
        customer_name,
        monetary,
        frequency,
        recency,

        NTILE(5) OVER (
            ORDER BY recency DESC
        ) AS r_score,

        NTILE(5) OVER (
            ORDER BY frequency
        ) AS f_score,

        NTILE(5) OVER (
            ORDER BY monetary
        ) AS m_score

    FROM customer_rfm
)

SELECT
    customer_name,
    monetary,
    frequency,
    recency,
    r_score,
    f_score,
    m_score,

    CASE

        WHEN r_score >= 4
             AND f_score >= 4
             AND m_score >= 4
        THEN 'Champions'

        WHEN r_score >= 4
             AND f_score >= 3
        THEN 'Clients fidèles'

        WHEN r_score >= 3
             AND m_score >= 3
        THEN 'Clients à potentiel'

        WHEN r_score <= 2
             AND m_score >= 4
        THEN 'À réactiver'

        ELSE 'Clients à risque'

    END AS rfm_segment

FROM rfm_scores

ORDER BY monetary DESC;
"""

cursor.execute(query)

results = cursor.fetchall()

print("\n========== SEGMENTATION RFM ==========")

for row in results[:30]:

    customer, monetary, frequency, recency, r, f, m, segment = row

    print(
        f"{customer} | "
        f"CA : {monetary:,.2f} $ | "
        f"Commandes : {frequency} | "
        f"Recency : {recency} jours | "
        f"Score : {r}{f}{m} | "
        f"Segment : {segment}"
    )
# ==========================================
# PERFORMANCE DES SEGMENTS RFM
# ==========================================

query = """
WITH customer_rfm AS (

    SELECT
        "Customer Name" AS customer_name,
        SUM(Sales) AS monetary,
        COUNT(DISTINCT "Order ID") AS frequency,

        CAST(
            julianday((SELECT MAX("Order Date") FROM sales))
            - julianday(MAX("Order Date"))
            AS INTEGER
        ) AS recency

    FROM sales
    GROUP BY "Customer Name"
),

rfm_scores AS (

    SELECT
        customer_name,
        monetary,
        frequency,
        recency,

        NTILE(5) OVER (ORDER BY recency DESC) AS r_score,

        NTILE(5) OVER (ORDER BY frequency) AS f_score,

        NTILE(5) OVER (ORDER BY monetary) AS m_score

    FROM customer_rfm
),

segmented AS (

    SELECT
        customer_name,
        monetary,
        frequency,
        recency,

        CASE

            WHEN r_score >= 4
                 AND f_score >= 4
                 AND m_score >= 4
            THEN 'Champions'

            WHEN r_score >= 4
                 AND f_score >= 3
            THEN 'Clients fidèles'

            WHEN r_score >= 3
                 AND m_score >= 3
            THEN 'Clients à potentiel'

            WHEN r_score <= 2
                 AND m_score >= 4
            THEN 'À réactiver'

            ELSE 'Clients à risque'

        END AS segment

    FROM rfm_scores
)

SELECT
    segment,
    COUNT(*) AS customers,
    ROUND(SUM(monetary), 2) AS total_sales,
    ROUND(AVG(monetary), 2) AS average_customer_value

FROM segmented

GROUP BY segment

ORDER BY total_sales DESC;
"""

cursor.execute(query)

results = cursor.fetchall()

print("\n========== PERFORMANCE DES SEGMENTS RFM ==========")

for segment, customers, sales, average_value in results:

    print(
        f"{segment} | "
        f"Clients : {customers} | "
        f"CA : {sales:,.2f} $ | "
        f"CA moyen/client : {average_value:,.2f} $"
    )

# ==========================================
# CRÉATION DE LA VUE CUSTOMER_RFM
# ==========================================

cursor.execute("DROP VIEW IF EXISTS customer_rfm")

query = """
CREATE VIEW customer_rfm AS

WITH customer_data AS (
    SELECT
        "Customer Name" AS customer_name,
        SUM(Sales) AS sales,
        COUNT(DISTINCT "Order ID") AS orders,
        MAX("Order Date") AS last_order_date
    FROM sales
    GROUP BY "Customer Name"
),

rfm_data AS (
    SELECT
        customer_name,
        sales,
        orders,
        CAST(
            julianday((SELECT MAX("Order Date") FROM sales))
            - julianday(last_order_date)
            AS INTEGER
        ) AS recency
    FROM customer_data
),

rfm_scores AS (
    SELECT
        customer_name,
        sales,
        orders,
        recency,

        NTILE(5) OVER (ORDER BY recency DESC) AS r_score,
        NTILE(5) OVER (ORDER BY orders ASC) AS f_score,
        NTILE(5) OVER (ORDER BY sales ASC) AS m_score

    FROM rfm_data
)

SELECT
    customer_name AS "Customer Name",
    ROUND(sales, 2) AS Sales,
    orders AS Orders,
    recency AS Recency,
    r_score AS "R Score",
    f_score AS "F Score",
    m_score AS "M Score",

    CAST(r_score AS TEXT)
    || CAST(f_score AS TEXT)
    || CAST(m_score AS TEXT)
    AS "RFM Score",

    CASE
        WHEN r_score >= 4
         AND f_score >= 4
         AND m_score >= 4
        THEN 'Champions'

        WHEN r_score >= 3
         AND f_score >= 4
        THEN 'Clients fidèles'

        WHEN r_score >= 3
         AND m_score >= 3
        THEN 'Clients à potentiel'

        WHEN r_score <= 2
         AND m_score >= 3
        THEN 'À réactiver'

        ELSE 'Clients à risque'
    END AS Segment

FROM rfm_scores;
"""

cursor.execute(query)

connection.commit()

print("\n========== VUE CUSTOMER_RFM CRÉÉE ==========")


# ==========================================
# VÉRIFICATION DE LA VUE CUSTOMER_RFM
# ==========================================

query = """
SELECT *
FROM customer_rfm
ORDER BY Sales DESC
LIMIT 20;
"""

cursor.execute(query)

results = cursor.fetchall()

print("\n========== APERÇU CUSTOMER_RFM ==========")

for row in results:
    print(row)


# ==========================================
# RÉPARTITION DES CLIENTS PAR SEGMENT RFM
# ==========================================

query = """
SELECT
    Segment,
    COUNT(*) AS clients,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(AVG(Sales), 2) AS average_sales_per_client
FROM customer_rfm
GROUP BY Segment
ORDER BY total_sales DESC;
"""

cursor.execute(query)

results = cursor.fetchall()

print("\n========== PERFORMANCE DES SEGMENTS RFM ==========")

for segment, clients, total_sales, average_sales in results:

    print(
        f"{segment} | "
        f"Clients : {clients} | "
        f"CA : {total_sales:,.2f} $ | "
        f"CA moyen/client : {average_sales:,.2f} $"
    )

# ==========================================
# EXPORT CUSTOMER_RFM POUR POWER BI
# ==========================================

query = """
SELECT
    "Customer Name",
    Sales,
    Orders,
    Recency,
    "R Score",
    "F Score",
    "M Score",
    "RFM Score",
    Segment
FROM customer_rfm;
"""

cursor.execute(query)

rows = cursor.fetchall()

columns = [
    "Customer Name",
    "Sales",
    "Orders",
    "Recency",
    "R Score",
    "F Score",
    "M Score",
    "RFM Score",
    "Segment"
         ]

import csv

customer_rfm_csv = base_dir / "data" / "customer_rfm.csv"

with open(customer_rfm_csv, "w", newline="", encoding="utf-8-sig") as file:

    writer = csv.writer(file)

    writer.writerow(columns)
    writer.writerows(rows)

print(f"\nFichier Power BI créé : {customer_rfm_csv}")
print(f"Nombre de clients exportés : {len(rows)}")

# ==========================================
# EXPORT SALES POUR POWER BI
# ==========================================

query = """
SELECT *
FROM sales;
"""

cursor.execute(query)

rows = cursor.fetchall()

columns = [description[0] for description in cursor.description]

sales_csv = base_dir / "data" / "sales.csv"

with open(sales_csv, "w", newline="", encoding="utf-8-sig") as file:

    writer = csv.writer(file)

    writer.writerow(columns)
    writer.writerows(rows)

print(f"\nFichier Power BI créé : {sales_csv}")
print(f"Nombre de lignes exportées : {len(rows)}")
# ==========================================
# FERMETURE
# ==========================================

connection.close()

# RFM  Recency → depuis combien de temps le client a acheté,Frequency → combien de commandes,Monetary → combien il dépense
#  NTILE(4) elle coupe le resulta en 4 segement nmeroter(1,2,3,4)