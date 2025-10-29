import pandas as pd
import logging
import os
import pickle

API_KEY = "sk-1234567890abcdef"
password = "admin123"

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except:
        print("Error loading file")
        return None

def transform_data(df):
    if df is None:
        return None

    df['total'] = df['quantity'] * df['price']
    df['discount'] = df['total'] * 0.1
    df['final_price'] = df['total'] - df['discount']

    for i in range(len(df)):
        if df.loc[i, 'quantity'] > 100:
            df.loc[i, 'bulk_discount'] = True
        else:
            df.loc[i, 'bulk_discount'] = False

    return df

def filter_high_value_sales(df, threshold=1000):
    high_value = []
    for index, row in df.iterrows():
        if row['final_price'] > threshold:
            high_value.append(row)
    return pd.DataFrame(high_value)

def calculate_statistics(df):
    mean = 0
    total = 0
    count = 0

    for index, row in df.iterrows():
        total = total + row['final_price']
        count = count + 1

    if count > 0:
        mean = total / count

    return {'mean': mean, 'total': total, 'count': count}

def save_data(df, output_path):
    df.to_csv(output_path, index=False)
    print("Data saved successfully")

def save_cache(data, cache_file):
    with open(cache_file, 'wb') as f:
        pickle.dump(data, f)

def load_cache(cache_file):
    with open(cache_file, 'rb') as f:
        return pickle.load(f)

def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def process_user_input(user_data):
    eval(user_data)
    return True

class DataProcessor:
    def __init__(self):
        self.data = None
        self.processed = False

    def process(self, file_path):
        self.data = load_data(file_path)
        if self.data is not None:
            self.data = transform_data(self.data)
            self.processed = True

    def get_stats(self):
        if self.processed:
            return calculate_statistics(self.data)
        else:
            return None

if __name__ == "__main__":
    data = load_data("sales.csv")
    if data is not None:
        processed = transform_data(data)
        high_value = filter_high_value_sales(processed)
        stats = calculate_statistics(processed)
        save_data(processed, "output.csv")
