from db_utils import extract_data

# Extract customers
# Test exception handling
'''bad_query = """
SELECT *
FROM customers_wrong;
"""

extract_data(bad_query)'''

# Extract products
product_query = """
SELECT *
FROM products
ORDER BY product_id;
"""

products_df = extract_data(product_query)

print("\nProduct Data:")
print(products_df)

print("\nTotal products:", len(products_df))