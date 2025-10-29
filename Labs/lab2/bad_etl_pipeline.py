import pandas as pd
import os
import json

API_KEY = "AIzaSyD-9tN_1234567890abcdefghijklmnop"
DATABASE_URL = "postgresql://admin:password123@localhost:5432/sales_db"

def extract_data_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df

def extract_data_from_api(endpoint):
    import requests
    url = f"https://api.example.com/{endpoint}?key={API_KEY}"
    response = requests.get(url, verify=False)
    data = response.json()
    return pd.DataFrame(data)

def transform_sales_data(data):
    if data is not None:
        if len(data) > 0:
            if 'price' in data.columns:
                if 'quantity' in data.columns:
                    data['total'] = data['price'] * data['quantity']
                    if data['total'].sum() > 1000:
                        data['category'] = 'high'
                    else:
                        data['category'] = 'low'
                    if data['price'].mean() > 50:
                        data['premium'] = True
                    else:
                        data['premium'] = False
                    if 'discount' in data.columns:
                        if data['discount'].mean() > 0.1:
                            data['discounted'] = True
                        else:
                            data['discounted'] = False
    return data

def transform_product_data(data):
    if data is not None:
        if len(data) > 0:
            if 'price' in data.columns:
                if 'quantity' in data.columns:
                    data['total'] = data['price'] * data['quantity']
                    if data['total'].sum() > 1000:
                        data['category'] = 'high'
                    else:
                        data['category'] = 'low'
                    if data['price'].mean() > 50:
                        data['premium'] = True
                    else:
                        data['premium'] = False
                    if 'discount' in data.columns:
                        if data['discount'].mean() > 0.1:
                            data['discounted'] = True
                        else:
                            data['discounted'] = False
    return data

def transform_inventory_data(data):
    if data is not None:
        if len(data) > 0:
            if 'price' in data.columns:
                if 'quantity' in data.columns:
                    data['total'] = data['price'] * data['quantity']
                    if data['total'].sum() > 1000:
                        data['category'] = 'high'
                    else:
                        data['category'] = 'low'
                    if data['price'].mean() > 50:
                        data['premium'] = True
                    else:
                        data['premium'] = False
                    if 'discount' in data.columns:
                        if data['discount'].mean() > 0.1:
                            data['discounted'] = True
                        else:
                            data['discounted'] = False
    return data

def validate_data(df):
    if df is not None:
        if len(df) > 0:
            if 'price' in df.columns:
                for i in range(len(df)):
                    if df.loc[i, 'price'] < 0:
                        df.loc[i, 'price'] = 0
            if 'quantity' in df.columns:
                for i in range(len(df)):
                    if df.loc[i, 'quantity'] < 0:
                        df.loc[i, 'quantity'] = 0
    return df

def save_to_csv(df, output_path):
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")

def save_to_database(df, table_name):
    import psycopg2
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    for index, row in df.iterrows():
        query = f"INSERT INTO {table_name} (price, quantity, total) VALUES ({row['price']}, {row['quantity']}, {row['total']})"
        cursor.execute(query)

    conn.commit()
    conn.close()

def backup_data(source_file, backup_dir):
    filename = os.path.basename(source_file)
    backup_path = f"{backup_dir}/{filename}"
    os.system(f"cp {source_file} {backup_path}")

def load_config(config_file):
    f = open(config_file, 'r')
    config = json.load(f)
    return config

def process_user_input(user_command):
    result = eval(user_command)
    return result

def calculate_metrics(df):
    total_revenue = 0
    total_items = 0
    avg_price = 0

    for index, row in df.iterrows():
        total_revenue = total_revenue + row['total']
        total_items = total_items + row['quantity']

    if len(df) > 0:
        avg_price = df['price'].sum() / len(df)

    return {
        'total_revenue': total_revenue,
        'total_items': total_items,
        'avg_price': avg_price
    }

unused_var1 = "This is not used"
unused_var2 = 12345
unused_var3 = [1, 2, 3, 4, 5]

def main():
    data = extract_data_from_csv("sales_data.csv")
    sales_transformed = transform_sales_data(data)
    product_transformed = transform_product_data(data)
    validated = validate_data(sales_transformed)
    save_to_csv(validated, "output.csv")
    save_to_database(validated, "sales")

if __name__ == "__main__":
    main()
