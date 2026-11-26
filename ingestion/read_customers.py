import psycopg
import pandas as pd

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "ecommerce_db",
    "user": "de_user",
    "password": "de_password_123"
}

# Connect to PostgreSQL
conn = psycopg.connect(**DB_CONFIG)

print("Database connection successful!")

# SQL query
query = """
SELECT
    customer_id,
    first_name,
    last_name,
    email,
    city,
    state,
    created_at
FROM customers
ORDER BY customer_id;
"""

# Extract data from PostgreSQL
cur = conn.cursor()
cur.execute(query)

rows = cur.fetchall()

# Convert database records into a Pandas DataFrame
columns = [column[0] for column in cur.description]

df = pd.DataFrame(rows, columns=columns)

# Close database resources
cur.close()
conn.close()

# Display the DataFrame
print("\nCustomer Data:")
print(df)

print("\nDataFrame Information:")
print(df.info())

print("\nNumber of records:", len(df))

# Display the DataFrame
print("\nCustomer Data:")
print(df)

# Dataset overview
print("\nDataset Overview:")
print("Total records:", len(df))
print("Total columns:", len(df.columns))

# Check missing values
print("\nMissing Values Per Column:")
print(df.isnull().sum())

# Display records with missing values
print("\nRecords With Missing Values:")
missing_customers = df[df.isnull().any(axis=1)]
print(missing_customers)

# Check duplicate rows
print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Check unique states
print("\nUnique States:")
print(df["state"].unique())

# Check unique cities
print("\nUnique Cities:")
print(df["city"].unique())

# Create a copy of the original data
clean_df = df.copy()

# City-to-state reference mapping
city_state_mapping = {
    "Indore": "Madhya Pradesh",
    "Hyderabad": "Telangana",
    "Mumbai": "Maharashtra",
    "Bengaluru": "Karnataka",
    "Pune": "Maharashtra",
    "Chennai": "Tamil Nadu",
    "Delhi": "Delhi",
    "Jaipur": "Rajasthan",
    "Kolkata": "West Bengal",
    "Ahmedabad": "Gujarat",
    "Lucknow": "Uttar Pradesh",
    "Chandigarh": "Punjab",
    "Surat": "Gujarat",
    "Coimbatore": "Tamil Nadu",
    "Nagpur": "Maharashtra"
}

# Fill missing states based on city mapping
missing_state_mask = clean_df["state"].isnull()

clean_df.loc[missing_state_mask, "state"] = (
    clean_df.loc[missing_state_mask, "city"]
    .map(city_state_mapping)
)

# Check the results
print("\nMissing States After Cleaning:")
print(clean_df["state"].isnull().sum())

print("\nCleaned Customer Records:")
print(clean_df)