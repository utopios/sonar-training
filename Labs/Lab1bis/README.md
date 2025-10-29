# Demo 01 - Introduction à SonarQube

## Objectif
Cette démo présente les fonctionnalités de base de SonarQube en comparant du code de mauvaise qualité avec du code de bonne qualité.

## Structure des fichiers

- `bad_code.py` - Code contenant intentionnellement des problèmes de qualité
- `good_code.py` - Version améliorée avec les bonnes pratiques
- `sonar-project.properties` - Configuration SonarQube pour le projet

## Types de problèmes détectés par SonarQube

### 1. Code Smells (Mauvaises pratiques)
- Variables non utilisées
- Code dupliqué
- Fonctions trop complexes
- Fonctions trop longues
- Magic numbers (nombres littéraux)
- Noms de variables non conformes
- Code mort (unreachable code)

### 2. Bugs
- Gestion d'exceptions trop large
- Division par zéro potentielle
- Comparaisons incorrectes avec True/False
- Code mort

### 3. Vulnérabilités de sécurité
- Mots de passe en dur
- Injection SQL potentielle
- Utilisation de eval() (exécution de code arbitraire)
- Clés API exposées

### 4. Problèmes de maintenance
- Absence de documentation
- Code de débogage (print statements)
- Complexité cyclomatique élevée
- Duplication de code

## Exécuter l'analyse SonarQube

### Prérequis
- SonarQube Server installé et en cours d'exécution
- SonarScanner CLI installé

### Commande d'analyse

```bash
# Depuis le dossier demos/01
sonar-scanner
```

### Ou avec Docker

```bash
docker run --rm \
  -e SONAR_HOST_URL="http://localhost:9000" \
  -v "$(pwd):/usr/src" \
  sonarsource/sonar-scanner-cli
```

## Comparaison des résultats attendus

### bad_code.py
- **Bugs**: ~5-8 détectés
- **Vulnérabilités**: ~3-4 détectées
- **Code Smells**: ~20-25 détectés
- **Complexité cyclomatique**: Élevée (>15)
- **Duplication**: ~30% de code dupliqué
- **Couverture de tests**: 0%

### good_code.py
- **Bugs**: 0
- **Vulnérabilités**: 0
- **Code Smells**: 0-2
- **Complexité cyclomatique**: Faible (<10)
- **Duplication**: 0%
- **Documentation**: Complète

## Points clés à observer

1. **Dashboard SonarQube**: Vue d'ensemble de la qualité du code
2. **Debt technique**: Temps estimé pour corriger tous les problèmes
3. **Hotspots de sécurité**: Points sensibles nécessitant une revue
4. **Tendances**: Evolution de la qualité au fil du temps
5. **Rules**: Règles violées avec explications détaillées

## Améliorations apportées dans good_code.py

### Avant (bad_code.py)
```python
# Problème: Magic number, pas de docstring
def calculate_area(radius):
    return 3.14159 * radius * radius
```

### Après (good_code.py)
```python
# Solution: Constante nommée, documentation complète, typing
PI = 3.14159

def calculate_circle_area(radius: float) -> float:
    """
    Calcule l'aire d'un cercle.

    Args:
        radius: Rayon du cercle

    Returns:
        float: Aire du cercle
    """
    return PI * radius * radius
```

## Exercices pratiques

1. Exécuter l'analyse SonarQube sur `bad_code.py`
2. Examiner chaque problème détecté dans l'interface SonarQube
3. Comparer avec l'analyse de `good_code.py`
4. Corriger progressivement les problèmes de `bad_code.py`
5. Re-exécuter l'analyse pour voir l'amélioration

## Ressources

- [Documentation SonarQube](https://docs.sonarqube.org/)
- [Règles Python SonarQube](https://rules.sonarsource.com/python/)
- [Clean Code de Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
