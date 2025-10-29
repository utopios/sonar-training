"""
Tests unitaires pour good_code.py
Ces tests couvrent les fonctions du fichier good_code.py (code de qualité)
"""

import pytest
import sys
import os
import tempfile
import logging
from unittest.mock import patch, MagicMock

# Ajouter le chemin src/app au path pour pouvoir importer good_code
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src/app'))

from good_code import (
    MembershipTier,
    PriceCalculation,
    simple_sum,
    calculate_price_with_discount,
    safe_division,
    safe_file_operation,
    calculate_circle_area,
    check_status,
    process_data,
    efficient_search,
    process_numbers,
    TAX_RATE,
    PI
)


class TestMembershipTier:
    """Tests pour l'énumération MembershipTier"""

    def test_bronze_value(self):
        assert MembershipTier.BRONZE.value == 0.05

    def test_silver_value(self):
        assert MembershipTier.SILVER.value == 0.10

    def test_gold_value(self):
        assert MembershipTier.GOLD.value == 0.15

    def test_tier_ordering(self):
        """Vérifie que les remises sont dans l'ordre croissant"""
        assert MembershipTier.BRONZE.value < MembershipTier.SILVER.value < MembershipTier.GOLD.value


class TestPriceCalculation:
    """Tests pour la dataclass PriceCalculation"""

    def test_creation(self):
        calc = PriceCalculation(
            base_price=100.0,
            tax=20.0,
            discount=10.0,
            final_price=110.0
        )
        assert calc.base_price == 100.0
        assert calc.tax == 20.0
        assert calc.discount == 10.0
        assert calc.final_price == 110.0

    def test_dataclass_equality(self):
        calc1 = PriceCalculation(100.0, 20.0, 10.0, 110.0)
        calc2 = PriceCalculation(100.0, 20.0, 10.0, 110.0)
        assert calc1 == calc2


class TestSimpleSum:
    """Tests pour simple_sum"""

    def test_all_positive(self):
        assert simple_sum(1, 2, 3, 4, 5) == 15

    def test_all_negative(self):
        assert simple_sum(-1, -2, -3) == 0

    def test_mixed_positive_negative(self):
        assert simple_sum(10, -5, 3, -2, 7) == 20

    def test_with_zero(self):
        assert simple_sum(0, 5, 10) == 15

    def test_single_positive(self):
        assert simple_sum(42) == 42

    def test_single_negative(self):
        assert simple_sum(-42) == 0

    def test_no_arguments(self):
        assert simple_sum() == 0


class TestCalculatePriceWithDiscount:
    """Tests pour calculate_price_with_discount"""

    def test_bronze_tier(self):
        result = calculate_price_with_discount(100.0, MembershipTier.BRONZE)
        assert result.base_price == 100.0
        assert result.tax == 20.0
        assert result.discount == 5.0
        assert result.final_price == 115.0

    def test_silver_tier(self):
        result = calculate_price_with_discount(100.0, MembershipTier.SILVER)
        assert result.base_price == 100.0
        assert result.tax == 20.0
        assert result.discount == 10.0
        assert result.final_price == 110.0

    def test_gold_tier(self):
        result = calculate_price_with_discount(100.0, MembershipTier.GOLD)
        assert result.base_price == 100.0
        assert result.tax == 20.0
        assert result.discount == 15.0
        assert result.final_price == 105.0

    def test_zero_price(self):
        result = calculate_price_with_discount(0.0, MembershipTier.BRONZE)
        assert result.base_price == 0.0
        assert result.tax == 0.0
        assert result.discount == 0.0
        assert result.final_price == 0.0

    def test_decimal_price(self):
        result = calculate_price_with_discount(99.99, MembershipTier.SILVER)
        assert abs(result.tax - 19.998) < 0.001
        assert abs(result.discount - 9.999) < 0.001
        assert abs(result.final_price - 109.989) < 0.001

    def test_large_price(self):
        result = calculate_price_with_discount(10000.0, MembershipTier.GOLD)
        assert result.tax == 2000.0
        assert result.discount == 1500.0
        assert result.final_price == 10500.0

    def test_returns_correct_type(self):
        result = calculate_price_with_discount(100.0, MembershipTier.BRONZE)
        assert isinstance(result, PriceCalculation)


class TestSafeDivision:
    """Tests pour safe_division"""

    def test_normal_division(self):
        assert safe_division(10.0, 2.0) == 5.0

    def test_division_by_zero(self):
        with patch('good_code.logger') as mock_logger:
            result = safe_division(10.0, 0.0)
            assert result is None
            mock_logger.warning.assert_called_once_with("Tentative de division par zéro")

    def test_negative_numbers(self):
        assert safe_division(-10.0, 2.0) == -5.0

    def test_negative_denominator(self):
        assert safe_division(10.0, -2.0) == -5.0

    def test_zero_numerator(self):
        assert safe_division(0.0, 5.0) == 0.0

    def test_decimal_division(self):
        result = safe_division(7.0, 3.0)
        assert abs(result - 2.333333) < 0.000001


class TestSafeFileOperation:
    """Tests pour safe_file_operation"""

    def test_read_existing_file(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write("Test content")
            temp_path = f.name

        try:
            result = safe_file_operation(temp_path)
            assert result == "Test content"
        finally:
            os.unlink(temp_path)

    def test_read_nonexistent_file(self):
        with patch('good_code.logger') as mock_logger:
            result = safe_file_operation("/nonexistent/path/file.txt")
            assert result is None
            mock_logger.error.assert_called()

    def test_read_file_with_utf8(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write("Contenu avec accents: éàù")
            temp_path = f.name

        try:
            result = safe_file_operation(temp_path)
            assert "éàù" in result
        finally:
            os.unlink(temp_path)

    def test_read_empty_file(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            temp_path = f.name

        try:
            result = safe_file_operation(temp_path)
            assert result == ""
        finally:
            os.unlink(temp_path)


class TestCalculateCircleArea:
    """Tests pour calculate_circle_area"""

    def test_unit_radius(self):
        assert abs(calculate_circle_area(1.0) - PI) < 0.00001

    def test_radius_five(self):
        expected = PI * 5 * 5
        assert abs(calculate_circle_area(5.0) - expected) < 0.00001

    def test_radius_zero(self):
        assert calculate_circle_area(0.0) == 0.0

    def test_decimal_radius(self):
        result = calculate_circle_area(2.5)
        expected = PI * 2.5 * 2.5
        assert abs(result - expected) < 0.00001

    def test_large_radius(self):
        result = calculate_circle_area(100.0)
        expected = PI * 100 * 100
        assert abs(result - expected) < 0.001


class TestCheckStatus:
    """Tests pour check_status"""

    def test_active_status(self):
        assert check_status(True) == "Active"

    def test_inactive_status(self):
        assert check_status(False) == "Inactive"


class TestProcessData:
    """Tests pour process_data"""

    def test_positive_value(self):
        with patch('good_code.logger') as mock_logger:
            result = process_data(10.0)
            assert result == 20.0
            mock_logger.info.assert_called_once_with("Traitement des données: 10.0")

    def test_negative_value(self):
        assert process_data(-5.0) == -10.0

    def test_zero_value(self):
        assert process_data(0.0) == 0.0

    def test_decimal_value(self):
        result = process_data(3.5)
        assert result == 7.0

    def test_logging_called(self):
        with patch('good_code.logger') as mock_logger:
            process_data(42.0)
            mock_logger.info.assert_called()


class TestEfficientSearch:
    """Tests pour efficient_search"""

    def test_no_common_elements(self):
        result = efficient_search([1, 2, 3], [4, 5, 6], [7, 8, 9])
        assert result == []

    def test_one_common_element(self):
        result = efficient_search([1, 2, 3], [2, 4, 5], [2, 6, 7])
        assert result == [2]

    def test_multiple_common_elements(self):
        result = efficient_search([1, 2, 3], [1, 2, 4], [1, 2, 5])
        assert set(result) == {1, 2}

    def test_empty_lists(self):
        result = efficient_search([], [], [])
        assert result == []

    def test_all_same_elements(self):
        result = efficient_search([1, 2, 3], [1, 2, 3], [1, 2, 3])
        assert set(result) == {1, 2, 3}

    def test_one_empty_list(self):
        result = efficient_search([1, 2, 3], [], [1, 2, 3])
        assert result == []

    def test_duplicate_elements_in_input(self):
        result = efficient_search([1, 1, 2, 2], [1, 2, 2], [1, 2])
        # Les résultats sont des sets, donc pas de doublons
        assert set(result) == {1, 2}


class TestProcessNumbers:
    """Tests pour process_numbers"""

    def test_returns_list(self):
        result = process_numbers()
        assert isinstance(result, list)

    def test_all_elements_even(self):
        result = process_numbers()
        for item in result:
            assert item % 2 == 0

    def test_all_elements_positive(self):
        result = process_numbers()
        assert all(item > 0 for item in result)

    def test_result_not_empty(self):
        result = process_numbers()
        assert len(result) > 0

    def test_specific_values(self):
        """Test que les valeurs sont correctement filtrées et transformées"""
        result = process_numbers()
        # Pour i=26: item = 52, item² = 2704 (pair et > 50)
        # Pour i=27: item = 54, item² = 2916 (pair et > 50)
        assert 2704 in result  # (26 * 2)² = 52² = 2704
        assert 2916 in result  # (27 * 2)² = 54² = 2916


class TestConstants:
    """Tests pour les constantes"""

    def test_tax_rate_value(self):
        assert TAX_RATE == 0.2

    def test_pi_value(self):
        assert abs(PI - 3.14159) < 0.00001


# Tests d'intégration
class TestIntegration:
    """Tests d'intégration pour vérifier l'interaction entre les fonctions"""

    def test_price_calculation_progression(self):
        """Vérifie que les prix finaux progressent correctement selon les tiers"""
        price = 200.0
        bronze = calculate_price_with_discount(price, MembershipTier.BRONZE)
        silver = calculate_price_with_discount(price, MembershipTier.SILVER)
        gold = calculate_price_with_discount(price, MembershipTier.GOLD)

        # Gold devrait être le moins cher (plus de remise)
        assert gold.final_price < silver.final_price < bronze.final_price

    def test_efficient_vs_simple_search(self):
        """Compare la recherche efficace avec un résultat attendu"""
        list1 = [1, 2, 3, 4, 5]
        list2 = [3, 4, 5, 6, 7]
        list3 = [4, 5, 6, 7, 8]

        result = efficient_search(list1, list2, list3)
        expected = {4, 5}
        assert set(result) == expected

    def test_safe_division_with_process_data(self):
        """Utilise safe_division avec le résultat de process_data"""
        processed = process_data(10.0)  # Retourne 20.0
        result = safe_division(processed, 4.0)
        assert result == 5.0

    def test_circle_area_with_simple_sum(self):
        """Calcule l'aire d'un cercle avec un rayon issu de simple_sum"""
        radius = simple_sum(1, 2, 3, 4)  # Retourne 10
        area = calculate_circle_area(float(radius))
        expected = PI * 10 * 10
        assert abs(area - expected) < 0.00001


# Tests de performance (optionnels)
class TestPerformance:
    """Tests de performance pour les fonctions critiques"""

    def test_efficient_search_with_large_lists(self):
        """Vérifie que efficient_search peut gérer de grandes listes"""
        large_list1 = list(range(10000))
        large_list2 = list(range(5000, 15000))
        large_list3 = list(range(7500, 12500))

        result = efficient_search(large_list1, large_list2, large_list3)
        # Devrait trouver les éléments entre 7500 et 9999
        assert len(result) > 0
        assert all(7500 <= x < 10000 for x in result)

    def test_process_numbers_execution_time(self):
        """Vérifie que process_numbers s'exécute rapidement"""
        import time
        start = time.time()
        result = process_numbers()
        end = time.time()
        execution_time = end - start

        # Devrait s'exécuter en moins d'une seconde
        assert execution_time < 1.0
        assert len(result) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=good_code", "--cov-report=html"])
