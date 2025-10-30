"""Formatting utility functions."""

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict


def format_currency(amount: Decimal, currency: str = "USD") -> str:
    """
    Format decimal amount as currency string.

    Args:
        amount: Amount to format.
        currency: Currency code (default: USD).

    Returns:
        str: Formatted currency string.
    """
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥"
    }

    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"


def format_date(date: datetime, format_type: str = "short") -> str:
    """
    Format datetime object as string.

    Args:
        date: Date to format.
        format_type: Format type ("short", "long", "iso").

    Returns:
        str: Formatted date string.
    """
    formats = {
        "short": "%m/%d/%Y",
        "long": "%B %d, %Y",
        "iso": "%Y-%m-%d",
        "datetime": "%Y-%m-%d %H:%M:%S"
    }

    format_string = formats.get(format_type, formats["short"])
    return date.strftime(format_string)


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format decimal as percentage string.

    Args:
        value: Value to format (0.15 = 15%).
        decimals: Number of decimal places.

    Returns:
        str: Formatted percentage string.
    """
    return f"{value * 100:.{decimals}f}%"


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes.

    Returns:
        str: Formatted size string.
    """
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = float(size_bytes)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.2f} {units[unit_index]}"


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to maximum length with suffix.

    Args:
        text: Text to truncate.
        max_length: Maximum length including suffix.
        suffix: Suffix to add when truncated.

    Returns:
        str: Truncated text.
    """
    if len(text) <= max_length:
        return text

    truncated_length = max_length - len(suffix)
    return text[:truncated_length] + suffix


def format_phone_number(phone: str) -> str:
    """
    Format phone number to standard format.

    Args:
        phone: Phone number to format.

    Returns:
        str: Formatted phone number.
    """
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, phone))

    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone


def camel_to_snake_case(text: str) -> str:
    """
    Convert camelCase to snake_case.

    Args:
        text: Text in camelCase.

    Returns:
        str: Text in snake_case.
    """
    import re
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()


def snake_to_camel_case(text: str) -> str:
    """
    Convert snake_case to camelCase.

    Args:
        text: Text in snake_case.

    Returns:
        str: Text in camelCase.
    """
    components = text.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def format_dict_as_table(data: list[Dict[str, Any]], headers: list[str]) -> str:
    """
    Format list of dictionaries as ASCII table.

    Args:
        data: List of dictionaries with data.
        headers: List of header names.

    Returns:
        str: Formatted table string.
    """
    if not data:
        return "No data available"

    # Calculate column widths
    col_widths = {header: len(header) for header in headers}
    for row in data:
        for header in headers:
            value = str(row.get(header, ""))
            col_widths[header] = max(col_widths[header], len(value))

    # Build header
    header_row = " | ".join(header.ljust(col_widths[header]) for header in headers)
    separator = "-+-".join("-" * col_widths[header] for header in headers)

    # Build rows
    rows = []
    for row in data:
        row_str = " | ".join(
            str(row.get(header, "")).ljust(col_widths[header])
            for header in headers
        )
        rows.append(row_str)

    return f"{header_row}\n{separator}\n" + "\n".join(rows)
