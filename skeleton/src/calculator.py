"""
Module de calculatrice simple pour la démonstration SonarQube
"""

class Calculator:
    """Classe Calculator pour effectuer des opérations mathématiques"""
    
    def add(self, a, b):
        """Additionne deux nombres"""
        return a + b
    
    def subtract(self, a, b):
        """Soustrait deux nombres"""
        return a - b
    
    def multiply(self, a, b):
        """Multiplie deux nombres"""
        return a * b
    
    def divide(self, a, b):
        """Divise deux nombres"""
        if b == 0:
            raise ValueError("Division par zéro impossible")
        return a / b
    
    def power(self, a, b):
        """Élève a à la puissance b"""
        return a ** b


def main():
    """Fonction principale"""
    calc = Calculator()
    print("2 + 3 =", calc.add(2, 3))
    print("10 - 4 =", calc.subtract(10, 4))
    print("5 * 6 =", calc.multiply(5, 6))
    print("15 / 3 =", calc.divide(15, 3))
    print("2 ^ 8 =", calc.power(2, 8))


if __name__ == "__main__":
    main()
