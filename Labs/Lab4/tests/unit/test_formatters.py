"""Unit tests for formatter utilities."""

import pytest
from datetime import datetime
from decimal import Decimal
from src.app.utils.formatters import (
    format_currency,
    format_date,
    format_percentage,
    format_file_size,
    truncate_text,
    format_phone_number,
    camel_to_snake_case,
    snake_to_camel_case,
    format_dict_as_table
)


class TestFormatters:
    """Test suite for formatter functions."""

    def test_format_currency_usd(self):
        """Test formatting currency in USD."""
        result = format_currency(Decimal("1234.56"), "USD")
        assert result == "$1,234.56"

    def test_format_currency_eur(self):
        """Test formatting currency in EUR."""
        result = format_currency(Decimal("999.99"), "EUR")
        assert result == "€999.99"

    def test_format_currency_gbp(self):
        """Test formatting currency in GBP."""
        result = format_currency(Decimal("500.00"), "GBP")
        assert result == "£500.00"

    def test_format_currency_jpy(self):
        """Test formatting currency in JPY."""
        result = format_currency(Decimal("10000.00"), "JPY")
        assert result == "¥10,000.00"

    def test_format_currency_unknown(self):
        """Test formatting currency with unknown code."""
        result = format_currency(Decimal("100.00"), "XYZ")
        assert result == "XYZ100.00"

    def test_format_currency_zero(self):
        """Test formatting zero amount."""
        result = format_currency(Decimal("0.00"), "USD")
        assert result == "$0.00"

    def test_format_currency_large_amount(self):
        """Test formatting large amount."""
        result = format_currency(Decimal("1000000.99"), "USD")
        assert result == "$1,000,000.99"

    def test_format_date_short(self):
        """Test formatting date in short format."""
        date = datetime(2024, 3, 15)
        result = format_date(date, "short")
        assert result == "03/15/2024"

    def test_format_date_long(self):
        """Test formatting date in long format."""
        date = datetime(2024, 3, 15)
        result = format_date(date, "long")
        assert result == "March 15, 2024"

    def test_format_date_iso(self):
        """Test formatting date in ISO format."""
        date = datetime(2024, 3, 15)
        result = format_date(date, "iso")
        assert result == "2024-03-15"

    def test_format_date_datetime(self):
        """Test formatting date with time."""
        date = datetime(2024, 3, 15, 14, 30, 45)
        result = format_date(date, "datetime")
        assert result == "2024-03-15 14:30:45"

    def test_format_date_default(self):
        """Test formatting date with default format."""
        date = datetime(2024, 3, 15)
        result = format_date(date)
        assert result == "03/15/2024"

    def test_format_date_invalid_format(self):
        """Test formatting date with invalid format type."""
        date = datetime(2024, 3, 15)
        result = format_date(date, "invalid")
        assert result == "03/15/2024"

    def test_format_percentage_default(self):
        """Test formatting percentage with default decimals."""
        result = format_percentage(0.15)
        assert result == "15.00%"

    def test_format_percentage_custom_decimals(self):
        """Test formatting percentage with custom decimals."""
        result = format_percentage(0.1234, 3)
        assert result == "12.340%"

    def test_format_percentage_zero(self):
        """Test formatting zero percentage."""
        result = format_percentage(0.0)
        assert result == "0.00%"

    def test_format_percentage_one_hundred(self):
        """Test formatting 100 percentage."""
        result = format_percentage(1.0)
        assert result == "100.00%"

    def test_format_percentage_over_one_hundred(self):
        """Test formatting percentage over 100."""
        result = format_percentage(1.5, 1)
        assert result == "150.0%"

    def test_format_file_size_bytes(self):
        """Test formatting file size in bytes."""
        result = format_file_size(500)
        assert result == "500.00 B"

    def test_format_file_size_kilobytes(self):
        """Test formatting file size in kilobytes."""
        result = format_file_size(2048)
        assert round(float(result.split()[0]), 2) == 2.00
        assert "KB" in result

    def test_format_file_size_megabytes(self):
        """Test formatting file size in megabytes."""
        result = format_file_size(5242880)  # 5 MB
        assert round(float(result.split()[0]), 2) == 5.00
        assert "MB" in result

    def test_format_file_size_gigabytes(self):
        """Test formatting file size in gigabytes."""
        result = format_file_size(3221225472)  # 3 GB
        assert round(float(result.split()[0]), 2) == 3.00
        assert "GB" in result

    def test_format_file_size_zero(self):
        """Test formatting zero file size."""
        result = format_file_size(0)
        assert result == "0.00 B"

    def test_truncate_text_no_truncation(self):
        """Test truncating text that doesn't need truncation."""
        result = truncate_text("Short text", 20)
        assert result == "Short text"

    def test_truncate_text_with_truncation(self):
        """Test truncating long text."""
        result = truncate_text("This is a very long text", 15)
        assert result == "This is a v..."
        assert len(result) == 15

    def test_truncate_text_custom_suffix(self):
        """Test truncating text with custom suffix."""
        result = truncate_text("Long text here", 10, ">>")
        assert result == "Long tex>>"
        assert len(result) == 10

    def test_truncate_text_exact_length(self):
        """Test truncating text at exact max length."""
        result = truncate_text("12345", 5)
        assert result == "12345"

    def test_format_phone_number_10_digits(self):
        """Test formatting 10-digit phone number."""
        result = format_phone_number("1234567890")
        assert result == "(123) 456-7890"

    def test_format_phone_number_11_digits(self):
        """Test formatting 11-digit phone number with country code."""
        result = format_phone_number("11234567890")
        assert result == "+1 (123) 456-7890"

    def test_format_phone_number_with_separators(self):
        """Test formatting phone number with existing separators."""
        result = format_phone_number("123-456-7890")
        assert result == "(123) 456-7890"

    def test_format_phone_number_invalid_length(self):
        """Test formatting phone number with invalid length."""
        result = format_phone_number("12345")
        assert result == "12345"

    def test_format_phone_number_with_spaces(self):
        """Test formatting phone number with spaces."""
        result = format_phone_number("123 456 7890")
        assert result == "(123) 456-7890"

    def test_camel_to_snake_case(self):
        """Test converting camelCase to snake_case."""
        result = camel_to_snake_case("camelCaseText")
        assert result == "camel_case_text"

    def test_camel_to_snake_case_multiple_capitals(self):
        """Test converting camelCase with multiple capitals."""
        result = camel_to_snake_case("thisIsATest")
        assert result == "this_is_a_test"

    def test_camel_to_snake_case_single_word(self):
        """Test converting single word."""
        result = camel_to_snake_case("word")
        assert result == "word"

    def test_camel_to_snake_case_already_lowercase(self):
        """Test converting already lowercase text."""
        result = camel_to_snake_case("lowercase")
        assert result == "lowercase"

    def test_snake_to_camel_case(self):
        """Test converting snake_case to camelCase."""
        result = snake_to_camel_case("snake_case_text")
        assert result == "snakeCaseText"

    def test_snake_to_camel_case_single_word(self):
        """Test converting single word."""
        result = snake_to_camel_case("word")
        assert result == "word"

    def test_snake_to_camel_case_multiple_underscores(self):
        """Test converting snake_case with multiple underscores."""
        result = snake_to_camel_case("this_is_a_test")
        assert result == "thisIsATest"

    def test_format_dict_as_table_simple(self):
        """Test formatting simple dictionary as table."""
        data = [
            {"name": "John", "age": "30"},
            {"name": "Jane", "age": "25"}
        ]
        headers = ["name", "age"]
        result = format_dict_as_table(data, headers)

        assert "name" in result
        assert "age" in result
        assert "John" in result
        assert "Jane" in result
        assert "|" in result
        assert "-" in result

    def test_format_dict_as_table_empty_data(self):
        """Test formatting empty data as table."""
        data = []
        headers = ["name", "age"]
        result = format_dict_as_table(data, headers)
        assert result == "No data available"

    def test_format_dict_as_table_missing_keys(self):
        """Test formatting table with missing keys in data."""
        data = [
            {"name": "John"},
            {"name": "Jane", "age": "25"}
        ]
        headers = ["name", "age"]
        result = format_dict_as_table(data, headers)

        assert "John" in result
        assert "Jane" in result

    def test_format_dict_as_table_wide_columns(self):
        """Test formatting table with wide column values."""
        data = [
            {"name": "VeryLongNameHere", "value": "ShortValue"}
        ]
        headers = ["name", "value"]
        result = format_dict_as_table(data, headers)

        assert "VeryLongNameHere" in result
        assert "ShortValue" in result
