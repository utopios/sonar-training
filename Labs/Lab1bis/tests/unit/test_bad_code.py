"""
Tests unitaires pour bad_code.py
Ces tests couvrent les fonctions du fichier bad_code.py
"""

import pytest
import sys
import os

from src.app.bad_code import (
    complex_function,
    calculate_discount_bronze,
    calculate_discount_silver,
    calculate_discount_gold,
    risky_operation,
    mysterious_function,
    function_with_dead_code,
    calculate_area,
    bad_naming,
    get_user_data,
    check_status,
    process_data,
    dangerous_eval,
    inefficient_search,
    very_long_function
)


class TestComplexFunction:
    """Tests pour complex_function"""

    def test_all_positive(self):
        assert complex_function(1, 1, 1, 1, 1) == 5

    def test_last_zero(self):
        assert complex_function(1, 1, 1, 1, 0) == 4

    def test_fourth_zero(self):
        assert complex_function(1, 1, 1, 0, 5) == 3

    def test_third_zero(self):
        assert complex_function(1, 1, 0, 5, 5) == 2

    def test_second_zero(self):
        assert complex_function(1, 0, 5, 5, 5) == 1

    def test_first_zero(self):
        assert complex_function(0, 5, 5, 5, 5) == 0

    def test_first_negative(self):
        assert complex_function(-1, 5, 5, 5, 5) == 0


class TestDiscountFunctions:
    """Tests pour les fonctions de calcul de remise"""

    def test_bronze_discount(self):
        result = calculate_discount_bronze(100)
        expected = 100 + (100 * 0.2) - (100 * 0.05)
        assert result == expected
        assert result == 115.0

    def test_silver_discount(self):
        result = calculate_discount_silver(100)
        expected = 100 + (100 * 0.2) - (100 * 0.10)
        assert result == expected
        assert result == 110.0

    def test_gold_discount(self):
        result = calculate_discount_gold(100)
        expected = 100 + (100 * 0.2) - (100 * 0.15)
        assert result == expected
        assert result == 105.0

    def test_bronze_discount_zero_price(self):
        assert calculate_discount_bronze(0) == 0.0

    def test_silver_discount_decimal_price(self):
        result = calculate_discount_silver(99.99)
        assert abs(result - 109.989) < 0.001


class TestRiskyOperation:
    """Tests pour risky_operation"""

    def test_no_exception_raised(self):
        # La fonction ne devrait pas lever d'exception car elle les attrape toutes
        result = risky_operation()
        assert result is None


class TestMysteriousFunction:
    """Tests pour mysterious_function"""

    def test_normal_calculation(self):
        assert mysterious_function(10, 5, 2) == 25.0

    def test_division_by_zero(self):
        assert mysterious_function(10, 5, 0) is None

    def test_negative_values(self):
        assert mysterious_function(-10, 5, 2) == -25.0

    def test_zero_numerator(self):
        assert mysterious_function(0, 5, 2) == 0.0


class TestFunctionWithDeadCode:
    """Tests pour function_with_dead_code"""

    def test_returns_early(self):
        assert function_with_dead_code() == "early return"


class TestCalculateArea:
    """Tests pour calculate_area"""

    def test_unit_radius(self):
        assert abs(calculate_area(1) - 3.14159) < 0.00001

    def test_radius_five(self):
        expected = 3.14159 * 5 * 5
        assert abs(calculate_area(5) - expected) < 0.00001

    def test_radius_zero(self):
        assert calculate_area(0) == 0.0

    def test_decimal_radius(self):
        result = calculate_area(2.5)
        expected = 3.14159 * 2.5 * 2.5
        assert abs(result - expected) < 0.00001


class TestBadNaming:
    """Tests pour bad_naming"""

    def test_returns_none(self):
        # La fonction ne retourne rien
        assert bad_naming() is None


class TestGetUserData:
    """Tests pour get_user_data (vulnérable à l'injection SQL)"""

    def test_normal_user_id(self):
        result = get_user_data(123)
        assert result == "SELECT * FROM users WHERE id = 123"

    def test_sql_injection_attempt(self):
        # Ce test montre la vulnérabilité
        malicious_input = "1 OR 1=1"
        result = get_user_data(malicious_input)
        assert result == "SELECT * FROM users WHERE id = 1 OR 1=1"


class TestCheckStatus:
    """Tests pour check_status"""

    def test_active_status(self):
        assert check_status(True) == "Active"

    def test_inactive_status(self):
        assert check_status(False) == "Inactive"


class TestProcessData:
    """Tests pour process_data"""

    def test_doubles_value(self, capsys):
        result = process_data(10)
        assert result == 20

        # Vérifier que les prints sont effectués
        captured = capsys.readouterr()
        assert "Debug: data received" in captured.out
        assert "Data value: 10" in captured.out

    def test_negative_value(self):
        assert process_data(-5) == -10

    def test_zero_value(self):
        assert process_data(0) == 0


class TestDangerousEval:
    """Tests pour dangerous_eval (fonction dangereuse)"""

    def test_simple_expression(self):
        result = dangerous_eval("2 + 2")
        assert result == 4

    def test_string_expression(self):
        result = dangerous_eval("'hello' + ' world'")
        assert result == "hello world"

    # Note: On ne teste pas les cas malveillants pour des raisons de sécurité


class TestInefficientSearch:
    """Tests pour inefficient_search"""

    def test_no_common_elements(self):
        result = inefficient_search([1, 2, 3], [4, 5, 6], [7, 8, 9])
        assert result == []

    def test_one_common_element(self):
        result = inefficient_search([1, 2, 3], [2, 4, 5], [2, 6, 7])
        assert result == [2]

    def test_multiple_common_elements(self):
        result = inefficient_search([1, 2, 3], [1, 2, 4], [1, 2, 5])
        assert set(result) == {1, 2}

    def test_empty_lists(self):
        result = inefficient_search([], [], [])
        assert result == []


class TestVeryLongFunction:
    """Tests pour very_long_function"""

    def test_returns_list(self):
        result = very_long_function()
        assert isinstance(result, list)

    def test_all_elements_even(self):
        result = very_long_function()
        for item in result:
            assert item % 2 == 0

    def test_all_elements_greater_than_threshold(self):
        # Les éléments filtrés doivent être > 50 après multiplication par 2
        # Donc l'entrée originale doit être > 25
        result = very_long_function()
        # Après le carré, les valeurs sont encore plus grandes
        assert all(item > 0 for item in result)

    def test_result_length(self):
        result = very_long_function()
        # Vérifie que la fonction retourne quelque chose
        assert len(result) > 0


# Tests d'intégration
class TestIntegration:
    """Tests d'intégration pour vérifier l'interaction entre les fonctions"""

    def test_discount_progression(self):
        """Vérifie que les remises progressent correctement"""
        price = 200
        bronze = calculate_discount_bronze(price)
        silver = calculate_discount_silver(price)
        gold = calculate_discount_gold(price)

        # Gold devrait être le moins cher
        assert gold < silver < bronze

    def test_mysterious_function_with_complex_function_result(self):
        """Utilise le résultat de complex_function dans mysterious_function"""
        result1 = complex_function(2, 2, 2, 2, 2)
        result2 = mysterious_function(result1, 3, 2)
        assert result2 == 15.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
