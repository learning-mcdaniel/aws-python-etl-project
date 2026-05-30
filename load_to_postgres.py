import pandas as pd
import psycopg2

# Load CSV
df = pd.read_csv("sales_clean.csv")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="postgres-etl-lab.c3k0ikys8001.us-east-2.rds.amazonaws.com",
    database="salesdb",
    user="postgres",
    password="Rocko46350"
)

cur = conn.cursor()

# Insert rows
for _, row in df.iterrows():
    cur.execute(
        """
        INSERT INTO sales (
            product_id,
            product_name,
            category,
            price_usd,
            quantity_sold,
            sales_amount,
            order_date,
            customer_city
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            row['product_id'],
            row['product_name'],
            row['category'],
            row['price_usd'],
            row['quantity_sold'],
            row['sales_amount'],
            row['order_date'],
            row['customer_city']
        )
    )

conn.commit()

print("Data loaded successfully.")

cur.close()
conn.close()
