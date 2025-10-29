from typing import List, Optional
import logging
from dataclasses import dataclass
from enum import Enum

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Constantes bien nommées
TAX_RATE = 0.2
PI = 3.14159


class MembershipTier(Enum):
    """Enumération des niveaux d'adhésion."""
    BRONZE = 0.05
    SILVER = 0.10
    GOLD = 0.15


@dataclass
class PriceCalculation:
    """Représente un calcul de prix avec taxes et remises."""
    base_price: float
    tax: float
    discount: float
    final_price: float


def simple_sum(*args: int) -> int:
    """
    Calcule la somme de nombres positifs.

    Args:
        *args: Nombres entiers à additionner

    Returns:
        int: La somme de tous les nombres positifs, 0 si tous sont négatifs
    """
    total = sum(arg for arg in args if arg > 0)
    return total if total > 0 else 0


def calculate_price_with_discount(
    base_price: float,
    tier: MembershipTier
) -> PriceCalculation:
    """
    Calcule le prix final avec taxes et remises selon le niveau d'adhésion.

    Args:
        base_price: Prix de base avant taxes et remises
        tier: Niveau d'adhésion du client

    Returns:
        PriceCalculation: Objet contenant tous les détails du calcul
    """
    tax = base_price * TAX_RATE
    discount = base_price * tier.value
    final_price = base_price + tax - discount

    return PriceCalculation(
        base_price=base_price,
        tax=tax,
        discount=discount,
        final_price=final_price
    )


def safe_division(numerator: float, denominator: float) -> Optional[float]:
    """
    Effectue une division sécurisée.

    Args:
        numerator: Le numérateur
        denominator: Le dénominateur

    Returns:
        Optional[float]: Le résultat de la division ou None si division par zéro
    """
    if denominator == 0:
        logger.warning("Tentative de division par zéro")
        return None
    return numerator / denominator


def safe_file_operation(filepath: str) -> Optional[str]:
    """
    Lit un fichier de manière sécurisée.

    Args:
        filepath: Chemin vers le fichier à lire

    Returns:
        Optional[str]: Contenu du fichier ou None en cas d'erreur
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé: {filepath}")
        return None
    except PermissionError:
        logger.error(f"Permission refusée pour: {filepath}")
        return None
    except Exception as error:
        logger.error(f"Erreur lors de la lecture de {filepath}: {error}")
        return None


def calculate_circle_area(radius: float) -> float:
    """
    Calcule l'aire d'un cercle.

    Args:
        radius: Rayon du cercle

    Returns:
        float: Aire du cercle
    """
    return PI * radius * radius


def check_status(is_active: bool) -> str:
    """
    Vérifie le statut d'activation.

    Args:
        is_active: État d'activation

    Returns:
        str: Statut textuel
    """
    return "Active" if is_active else "Inactive"


def process_data(data: float) -> float:
    """
    Traite les données en les multipliant par 2.

    Args:
        data: Valeur à traiter

    Returns:
        float: Valeur traitée
    """
    logger.info(f"Traitement des données: {data}")
    return data * 2


def efficient_search(list1: List[int], list2: List[int], list3: List[int]) -> List[int]:
    """
    Recherche efficace des éléments communs dans trois listes.

    Args:
        list1: Première liste
        list2: Deuxième liste
        list3: Troisième liste

    Returns:
        List[int]: Éléments présents dans les trois listes
    """
    # Utilisation de sets pour une recherche O(n) au lieu de O(n³)
    set1 = set(list1)
    set2 = set(list2)
    set3 = set(list3)

    return list(set1.intersection(set2, set3))


def process_numbers() -> List[int]:
    """
    Traite une séquence de nombres avec plusieurs transformations.

    Returns:
        List[int]: Nombres traités
    """
    data = list(range(100))

    # Pipeline de traitement clair et concis
    result = [
        item ** 2
        for item in (item * 2 for item in data)
        if item > 50 and item ** 2 % 2 == 0
    ]

    return result


def main() -> None:
    """Point d'entrée principal du programme."""
    logger.info("Exécution du code de qualité")

    # Exemple d'utilisation
    price_calc = calculate_price_with_discount(100.0, MembershipTier.GOLD)
    logger.info(f"Prix final calculé: {price_calc.final_price}")


if __name__ == "__main__":
    main()