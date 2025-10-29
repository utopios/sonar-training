import pytest
from data_validator import validate_email, validate_phone

def test_validate_email():
    assert validate_email('test@example.com') == True
    assert validate_email('invalid') == False
