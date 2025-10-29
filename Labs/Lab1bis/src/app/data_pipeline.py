import pandas as pd
import logging

def load_data(file_path):
    """Load CSV data"""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        logging.error("File not found")
        return None

def transform_data(df):
    """Transform data"""
    df['total'] = df['quantity'] * df['price']
    df['discount'] = df['total'] * 0.1
    return df

def save_data(df, output_path):
    """Save processed data"""
    df.to_csv(output_path, index=False)
    print("Data saved successfully")

# Main execution
if __name__ == "__main__":
    data = load_data("sales.csv")
    if data is not None:
        processed = transform_data(data)
        save_data(processed, "output.csv")