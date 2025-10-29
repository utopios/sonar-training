import pytest
import pandas as pd
from src.app.data_pipeline import load_data, transform_data, save_data

def test_transform_data():
    df = pd.DataFrame({
        'quantity': [10, 20],
        'price': [5.0, 10.0]
    })
    result = transform_data(df)
    assert 'total' in result.columns
    assert result['total'][0] == 50.0