"""
Tests unitaires pour le module calculator
"""
import unittest
import sys
sys.path.insert(0, '../src')
from src.calculator import Calculator


class TestCalculator(unittest.TestCase):
    """Classe de tests pour Calculator"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.calc = Calculator()
    
    def test_add(self):
        """Test de l'addition"""
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)
    
    def test_subtract(self):
        """Test de la soustraction"""
        self.assertEqual(self.calc.subtract(10, 4), 6)
        self.assertEqual(self.calc.subtract(5, 5), 0)
    
    def test_multiply(self):
        """Test de la multiplication"""
        self.assertEqual(self.calc.multiply(5, 6), 30)
        self.assertEqual(self.calc.multiply(0, 100), 0)
    
    def test_divide(self):
        """Test de la division"""
        self.assertEqual(self.calc.divide(15, 3), 5)
        self.assertEqual(self.calc.divide(10, 2), 5)
    
    def test_divide_by_zero(self):
        """Test de la division par zéro"""
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)
    
    def test_power(self):
        """Test de la puissance"""
        self.assertEqual(self.calc.power(2, 8), 256)
        self.assertEqual(self.calc.power(10, 2), 100)


if __name__ == '__main__':
    unittest.main()
