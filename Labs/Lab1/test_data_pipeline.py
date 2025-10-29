import pytest
import pandas as pd
from data_pipeline import load_data, transform_data, calculate_statistics

def test_transform_data():
    df = pd.DataFrame({
        'quantity': [10, 20],
        'price': [5.0, 10.0]
    })
    result = transform_data(df)
    assert 'total' in result.columns
    assert result['total'][0] == 50.0

def test_calculate_statistics():
    df = pd.DataFrame({
        'quantity': [10, 20],
        'price': [5.0, 10.0],
        'final_price': [50.0, 200.0]
    })
    stats = calculate_statistics(df)
    assert stats['count'] == 2
    assert stats['total'] == 250.0
